# -*- coding: utf-8 -*-
import azure.functions as func
from pip_services3_commons.commands import ICommandable, CommandSet, ICommand
from pip_services3_commons.convert import JsonConverter
from pip_services3_commons.run import Parameters

from .AzureFunctionService import AzureFunctionService
from ..containers.AzureFunctionContextHelper import AzureFunctionContextHelper


class CommandableAzureFunctionService(AzureFunctionService):
    """
    Abstract service that receives commands via Azure Function protocol
    to operations automatically generated for commands defined in :class:`ICommandable <pip_services3_commons.commands.ICommandable.ICommandable>` components.
    Each command is exposed as invoke method that receives command name and parameters.

    Commandable services require only 3 lines of code to implement a robust external
    Azure Function-based remote interface.

    This service is intended to work inside Azure Function container that
    exploses registered actions externally.

    ### Configuration parameters ###
        - dependencies:
            - controller:            override for Controller dependency

    ### References ###
        - `*:logger:*:*:1.0`            (optional) :class:`ILogger <pip_services3_components.log.ILogger.ILogger>`  components to pass log messages
        - `*:counters:*:*:1.0`          (optional) :class:`ICounters <pip_services3_components.count.ICounters.ICounters>`  components to pass collected measurements

    See: :class:`AzureFunctionService <pip_services3_azure.services.AzureFunctionService.AzureFunctionService>`

    Example:

    .. code-block:: python
        class MyCommandableAzureFunctionService(CommandableAzureFunctionService):
            def __init__(self):
                super(MyCommandableAzureFunctionService, self).__init__()
                self._dependency_resolver.put(
                    "controller", Descriptor("mygroup", "controller", "*", "*", "1.0")
                )


        service = MyCommandableAzureFunctionService()
        service.set_references(References.fromTuples(
            Descriptor("mygroup", "controller", "default", "default", "1.0"), controller
        ))

        service.open("123")
        print("The Azure Function service is running")

    """

    def __init__(self, name: str):
        """
        Creates a new instance of the service.

        :param name: a service name.
        """
        super(CommandableAzureFunctionService, self).__init__(name)
        self._dependency_resolver.put('controller', 'none')

        self._command_set: CommandSet = None

    def _get_parameters(self, context: func.HttpRequest) -> Parameters:
        """
        Returns body from Azure Function context.
        This method can be overloaded in child classes

        :param context: Azure Function context
        :return: Returns Parameters from context
        """
        return AzureFunctionContextHelper.get_parameters(context)

    def register(self):
        """
        Registers all actions in Azure Function.
        """
        controller: ICommandable = self._dependency_resolver.get_one_required('controller')
        self._command_set = controller.get_command_set()

        commands = self._command_set.get_commands()
        for index in range(len(commands)):
            command = commands[index]
            name = command.get_name()

            def wrapper(command: ICommand):
                # wrapper for passing context
                def action(context: func.HttpRequest):
                    correlation_id = self._get_correlation_id(context)
                    args = self._get_parameters(context)
                    if 'correlation_id' in args.keys():
                        args.remove('correlation_id')

                    timing = self._instrument(correlation_id, command.get_name())
                    try:
                        return command.execute(correlation_id, args)
                    except Exception as e:
                        timing.end_failure(e)
                        return func.HttpResponse(
                            body=JsonConverter.to_json(e),
                            status_code=400
                        )
                    finally:
                        timing.end_timing()

                return action

            self._register_action(name, None, wrapper(command))
