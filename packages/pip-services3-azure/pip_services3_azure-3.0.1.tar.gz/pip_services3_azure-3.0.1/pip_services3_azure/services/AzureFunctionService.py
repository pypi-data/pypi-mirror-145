# -*- coding: utf-8 -*-
import json
from abc import abstractmethod
from typing import Optional, List, Any, Callable

import azure.functions as func
from pip_services3_commons.config import IConfigurable, ConfigParams
from pip_services3_commons.errors import BadRequestException
from pip_services3_commons.refer import IReferenceable, DependencyResolver, IReferences
from pip_services3_commons.run import IOpenable
from pip_services3_commons.validate import Schema
from pip_services3_components.count import CompositeCounters
from pip_services3_components.log import CompositeLogger
from pip_services3_components.trace import CompositeTracer
from pip_services3_rpc.services import InstrumentTiming

from .AzureFunctionAction import AzureFunctionAction
from .IAzureFunctionService import IAzureFunctionService
from ..containers.AzureFunctionContextHelper import AzureFunctionContextHelper


class AzureFunctionService(IAzureFunctionService, IOpenable, IConfigurable, IReferenceable):
    """
    Abstract service that receives remove calls via Azure Function protocol.

    This service is intended to work inside AzureFunction container that
    exposes registered actions externally.

    ### Configuration parameters ###
        - dependencies:
            - controller:            override for Controller dependency

    ### References ###
        - `*:logger:*:*:1.0`            (optional) :class:`ILogger <pip_services3_components.log.ILogger.ILogger>`  components to pass log messages
        - `*:counters:*:*:1.0`          (optional) :class:`ICounters <pip_services3_components.count.ICounters.ICounters>`  components to pass collected measurements

    Example:

    .. code-block:: python

        class MyAzureFunctionService(AzureFunctionService):
            def __init__(self):
                super().__init__('v1.myservice')
                self._dependency_resolver.put(
                    "controller",
                    Descriptor("mygroup", "controller", "*", "*", "1.0")
                )
                self.__controller: IMyController = None

            def set_references(self, references: IReferences):
                super().set_references(references)
                self.__controller = self._dependency_resolver.get_required("controller")

            def __get_mydata(self, context: HttpRequest):
                data = context.get_json()
                correlation_id = data.get('correlation_id')
                id = data.get('id')
                return self.__controller.get_my_data(correlation_id, id)

            def register(self):
                self._register_action(
                    'get_mydata',
                    None,
                    self.__get_mydata
                )
                ...

        service = MyAzureFunctionService()
        service.configure(ConfigParams.from_tuples(
            "connection.protocol", "http",
            "connection.host", "localhost",
            "connection.port", 8080
        ))
        service.set_references(References.fromTuples(
            Descriptor("mygroup", "controller", "default", "default", "1.0"), controller
        ))
        service.open("123")

    """

    def __init__(self, name: Optional[str]):
        """
        Creates an instance of this service.

        :param name: a service name to generate action cmd.
        """
        self.__name = name

        self.__actions: List[AzureFunctionAction] = []
        self.__interceptors: list = []
        self.__opened: bool = False

        # The dependency resolver.
        self._dependency_resolver: DependencyResolver = DependencyResolver()

        # The logger.
        self._logger: CompositeLogger = CompositeLogger()

        # The performance counters.
        self._counters: CompositeCounters = CompositeCounters()

        # The tracer.
        self._tracer: CompositeTracer = CompositeTracer()

    def configure(self, config: ConfigParams):
        """
        Configures component by passing configuration parameters.

        :param config: configuration parameters to be set.
        """
        self._dependency_resolver.configure(config)

    def set_references(self, references: IReferences):
        """
        Sets references to dependent components.

        :param references: references to locate the component dependencies.
        """
        self._logger.set_references(references)
        self._counters.set_references(references)
        self._tracer.set_references(references)
        self._dependency_resolver.set_references(references)

    def get_actions(self) -> List[AzureFunctionAction]:
        """
        Get all actions supported by the service.

        :return: an array with supported actions.
        """
        return self.__actions

    def _instrument(self, correlation_id: Optional[str], name: str) -> InstrumentTiming:
        """
        Adds instrumentation to log calls and measure call time.
        It returns a Timing object that is used to end the time measurement.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :param name: a method name.
        :return: Timing object to end the time measurement.
        """
        self._logger.trace(correlation_id, "Executing %s method", name)
        self._counters.increment_one(name + ".exec_count")

        counter_timing = self._counters.begin_timing(name + ".exec_time")
        trace_timing = self._tracer.begin_trace(correlation_id, name, None)
        return InstrumentTiming(correlation_id, name, "exec",
                                self._logger, self._counters, counter_timing, trace_timing)

    def is_open(self) -> bool:
        """
        Checks if the component is opened.

        :return: true if the component has been opened and false otherwise.
        """
        return self.__opened

    def open(self, correlation_id: Optional[str]):
        """
        Opens the component.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        """
        if self.__opened:
            return

        self.register()

        self.__opened = True

    def close(self, correlation_id: Optional[str]):
        """
        Closes component and frees used resources.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        """
        if not self.__opened:
            return

        self.__opened = False
        self.__actions = []
        self.__interceptors = []

    def _apply_validation(self, schema: Schema, action: Callable[[func.HttpRequest], func.HttpResponse]) -> Callable[
        [func.HttpRequest], func.HttpResponse]:
        # Create an action function
        def action_wrapper(context: func.HttpRequest) -> func.HttpResponse:
            # Validate object
            if schema and context:
                # Perform validation
                params = {'body': {} if not context.get_body() else context.get_json()}
                params.update(context.route_params)
                params.update(context.params)

                correlation_id = self._get_correlation_id(context)
                err = schema.validate_and_return_exception(correlation_id, params, False)
                if err is not None:
                    return func.HttpResponse(
                        body=json.dumps(err.to_json()),
                        status_code=err.status
                    )

            result = action(context)
            return result

        return action_wrapper

    def _apply_interceptors(self, action: Callable[[func.HttpRequest], Any]) -> Callable[[func.HttpRequest], Any]:
        action_wrapper = action

        index = len(self.__interceptors) - 1
        while index >= 0:
            interceptor = self.__interceptors[index]
            action_wrapper = lambda _action: lambda params: interceptor(params, _action)(action_wrapper)

            index -= 1

        return action_wrapper

    def _generate_action_cmd(self, name: str) -> str:
        cmd = name
        if self.__name:
            cmd = self.__name + '.' + cmd
        return cmd

    def _register_action(self, name: str, schema: Schema, action: Callable[[func.HttpRequest], func.HttpResponse]):
        """
        Registers a action in Azure Function function.

        :param name: an action name
        :param schema: a validation schema to validate received parameters.
        :param action: an action function that is called when operation is invoked.
        """
        action_wrapper = self._apply_validation(schema, action)
        action_wrapper = self._apply_interceptors(action_wrapper)

        register_action: AzureFunctionAction = AzureFunctionAction(self._generate_action_cmd(name), schema,
                                                                   lambda params: action_wrapper(params))

        self.__actions.append(register_action)

    def _register_action_with_auth(self, name: str, schema: Schema,
                                   authorize: Callable[[func.HttpRequest, Callable[[func.HttpRequest], Any]], Any],
                                   action: Callable[[func.HttpRequest], func.HttpResponse]):
        """
        Registers an action with authorization.

        :param name: an action name
        :param schema: a validation schema to validate received parameters.
        :param authorize: an authorization interceptor
        :param action: an action function that is called when operation is invoked.
        """
        action_wrapper = self._apply_validation(schema, action)

        # Add authorization just before validation
        action_wrapper = lambda call: authorize(call, action_wrapper)

        action_wrapper = self._apply_interceptors(action_wrapper)

        register_action: AzureFunctionAction = AzureFunctionAction(self._generate_action_cmd(name), schema,
                                                                   lambda params: action_wrapper(params))

        self.__actions.append(register_action)

    def _register_interceptor(self, action: Callable[[func.HttpRequest, Callable[[func.HttpRequest], Any]], Any]):
        """
        Registers a middleware for actions in AWS Lambda service.

        :param action: an action function that is called when middleware is invoked.
        """
        self.__interceptors.append(action)

    @abstractmethod
    def register(self):
        """
        Registers all service routes in HTTP endpoint.

        This method is called by the service and must be overridden
        in child classes.
        """

    def _get_correlation_id(self, context: func.HttpRequest) -> str:
        """
        Returns correlationId from Azure Function context.
        This method can be overloaded in child classes

        :param context: the context context
        :return: returns correlationId from context
        """
        return AzureFunctionContextHelper.get_correlation_id(context)

    def _get_command(self, context: func.HttpRequest) -> str:
        """
        Returns command from Azure Function context.
        This method can be overloaded in child classes

        :param context: the context context
        :return: returns command from context
        """
        return AzureFunctionContextHelper.get_command(context)

    def act(self, context: func.HttpRequest) -> func.HttpResponse:
        """
        Calls registered action in this Azure Function.
        "cmd" parameter in the action parameters determine
        what action shall be called.

        This method shall only be used in testing.

        :param context: the context context.
        """
        cmd = self._get_command(context)
        correlation_id = self._get_correlation_id(context)

        if not cmd:
            raise BadRequestException(
                correlation_id,
                'NO_COMMAND',
                'Cmd parameter is missing'
            )

        filtered = list(filter(lambda a: a.cmd == cmd, self.__actions))
        action: AzureFunctionAction = None if len(filtered) == 0 else filtered[0]
        if not action:
            raise BadRequestException(
                correlation_id,
                'NO_ACTION',
                'Action ' + cmd + ' was not found'
            ).with_details('command', cmd)

        return action.action(context)
