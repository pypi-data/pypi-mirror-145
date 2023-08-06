# -*- coding: utf-8 -*-
from copy import deepcopy
from typing import Any, Optional

import requests
from requests.adapters import HTTPAdapter

from urllib3 import Retry

from pip_services3_commons.config import IConfigurable, ConfigParams
from pip_services3_commons.data import IdGenerator
from pip_services3_commons.errors import ConnectionException, UnknownException, ApplicationExceptionFactory
from pip_services3_commons.refer import IReferenceable, DependencyResolver, IReferences
from pip_services3_commons.run import IOpenable
from pip_services3_components.count import CompositeCounters
from pip_services3_components.log import CompositeLogger
from pip_services3_components.trace import CompositeTracer
from pip_services3_rpc.services import InstrumentTiming


from ..connect.AzureConnectionParams import AzureConnectionParams
from ..connect.AzureConnectionResolver import AzureConnectionResolver


class AzureFunctionClient(IOpenable, IConfigurable, IReferenceable):
    """
    Abstract client that calls Azure Functions.

    When making calls "cmd" parameter determines which what action shall be called, while
    other parameters are passed to the action itself.

    ### Configuration parameters ###
        - connections:
            - uri:                         (optional) full connection string or use protocol, app_name and function_name to build
            - protocol:                    (optional) connection protocol
            - app_name:                    (optional) Azure Function application name
            - function_name:               (optional) Azure Function name
        - credentials:
            - auth_code:                   Azure Function auth code if use custom authorization provide empty string

    ### References ###
        - `*:logger:*:*:1.0`            (optional) :class:`ILogger <pip_services3_components.log.ILogger.ILogger>`  components to pass log messages
        - `*:counters:*:*:1.0`          (optional) :class:`ICounters <pip_services3_components.count.ICounters.ICounters>`  components to pass collected measurements
        - `*:discovery:*:*:1.0`        (optional) :class:`IDiscovery <pip_services3_components.connect.IDiscovery.IDiscovery>` services to resolve connection
        - `*:credential-store:*:*:1.0`   (optional) Credential stores to resolve credentials

    See :class:`AzureFunction <pip_services3_azure.containers.AzureFunction.AzureFunction>` (in the Pip.Services components package),
    :class:`CommandableAzureClient <pip_services3_azure.clients.CommandableAzureClient.CommandableAzureClient>` (in the Pip.Services components package)

    .. code-block:: python

        class MyAzureFunctionClient(AzureFunctionClient, IMyClient):
            ...

            def get_data(self, correlation_id: Optional[str], id: str) -> MyData:

                timing = self._instrument(correlation_id, 'myclient.get_data')
                result = self._call('get_data', correlation_id, {'id': id}
                timing.end_timing()
                return result

            ...

        client = MyAzureFunctionClient()
        client.configure(ConfigParams.from_tuples(
            "connection.uri", "http://myapp.azurewebsites.net/api/myfunction",
            "connection.protocol", "http",
            "connection.app_name", "myapp",
            "connection.function_name", "myfunction"
            "credential.auth_code", "XXXX"
        ))

        result = client.get_data('123', '1')

    """

    def __init__(self):
        # The HTTP client.
        self._client: requests.Session = None
        # The Azure Function connection parameters
        self._connection: AzureConnectionParams = AzureConnectionParams()
        # The number of retries
        self._retries: int = 1
        # The default headers to be added to every request.
        self._headers = {}
        # The connection timeout in milliseconds.
        self._connection_timeout: int = 10000
        # The invocation timeout in milliseconds.
        self._timeout: int = 10000
        # The remote service uri which is calculated on open.
        self._uri: str = None
        # The dependencies resolver.
        self._dependency_resolver: DependencyResolver = DependencyResolver()
        # The connection resolver.
        self._connection_resolver: AzureConnectionResolver = AzureConnectionResolver()
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
        self._connection_resolver.configure(config)
        self._dependency_resolver.configure(config)

        self._connection_timeout = config.get_as_integer_with_default('options.connect_timeout',
                                                                      self._connection_timeout)

    def set_references(self, references: IReferences):
        """
        Sets references to dependent components.

        :param references: references to locate the component dependencies.
        """
        self._logger.set_references(references)
        self._counters.set_references(references)
        self._connection_resolver.set_references(references)
        self._dependency_resolver.set_references(references)

    def _instrument(self, correlation_id: Optional[str], name: str) -> InstrumentTiming:
        """
        Adds instrumentation to log calls and measure call time.
        It returns a CounterTiming object that is used to end the time measurement.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :param name: a method name.
        :return: object to end the time measurement.
        """
        self._logger.trace(correlation_id, "Executing %s method", name)
        self._counters.increment_one(name + ".exec_count")

        counter_timing = self._counters.begin_timing(name + '.exec_time')
        trace_timing = self._tracer.begin_trace(correlation_id, name, None)
        return InstrumentTiming(correlation_id, name, "exec",
                                self._logger, self._counters, counter_timing, trace_timing)

    def is_open(self) -> bool:
        """
        Checks if the component is opened.

        :return: true if the component has been opened and false otherwise.
        """
        return self._client is not None

    def open(self, correlation_id: Optional[str]):
        """
        Opens the component.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        """
        if self.is_open():
            return

        self._connection = self._connection_resolver.resolve(correlation_id)
        self._headers['x-functions-key'] = self._connection.get_auth_code()
        self._uri = self._connection.get_function_uri()

        try:
            self._client = requests.Session()
            self._client.headers.update(self._headers)

            adapter = HTTPAdapter(max_retries=Retry(
                total=self._retries,
                backoff_factor=self._timeout / 1000,
            ))

            self._client.mount("https://", adapter)
            self._client.mount("http://", adapter)
            self._client.params = {
                'url': self._uri,
                'timeout': (self._connection_timeout / 1000, self._timeout / 1000),
            }

            self._logger.debug(correlation_id, "Azure function client connected to %s",
                               self._connection.get_function_uri())
        except Exception as err:
            self._client.close()
            self._client = None

            raise ConnectionException(
                correlation_id, "CANNOT_CONNECT", "Connection to Azure function service failed"
            ).wrap(err).with_details("url", self._uri)

    def close(self, correlation_id: Optional[str]):
        if not self.is_open():
            return

        if self._client is not None:
            # Eat exceptions
            try:
                self._client.close()
                self._logger.debug(correlation_id, "Closed Azure function service at %s", self._uri)
            except Exception as err:
                self._logger.warn(correlation_id, 'Failed while closing Azure function service: %s', err)

            self._client = None
            self._uri = None

    def _invoke(self, cmd: str, correlation_id: Optional[str], args: dict) -> Any:
        """
        Performs Azure Function invocation.

        :param cmd: an action name to be called.
        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :param args: action arguments
        :return: action result.
        """
        if not cmd:
            raise UnknownException(None, 'NO_COMMAND', 'Missing Seneca pattern cmd')

        args = deepcopy(args or {})
        args['cmd'] = cmd
        args['correlation_id'] = correlation_id or IdGenerator.next_short()

        response = self._client.post(self._uri, json=args)

        if response.status_code == 204:
            return

        data = {} if not response.content else response.json()

        if response.status_code >= 400:
            raise ApplicationExceptionFactory.create(data).with_cause(Exception(response.text))

        return data

    def _call(self, cmd: str, correlation_id: Optional[str], params: dict = None) -> Any:
        """
        Calls a Azure Function action.

        :param cmd: an action name to be called.
        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :param params: (optional) action parameters.
        :return: action result.
        """
        return self._invoke(cmd, correlation_id, params)
