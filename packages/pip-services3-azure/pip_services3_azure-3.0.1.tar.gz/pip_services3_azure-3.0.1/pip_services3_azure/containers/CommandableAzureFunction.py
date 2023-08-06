# -*- coding: utf-8 -*-
import json
from typing import Optional

import azure.functions as func
from pip_services3_commons.commands import CommandSet, ICommandable, ICommand
from pip_services3_commons.convert import JsonConverter
from pip_services3_commons.run import Parameters
from pip_services3_rpc.services import InstrumentTiming

from .AzureFunction import AzureFunction
from .AzureFunctionContextHelper import AzureFunctionContextHelper


class CommandableAzureFunction(AzureFunction):
    """
    Abstract Azure Function function, that acts as a container to instantiate and run components
    and expose them via external entry point. All actions are automatically generated for commands
    defined in :class:`ICommandable <pip_services3_commons.commands.ICommandable.ICommandable>`. Each command is exposed as an action defined by "cmd" parameter.
    
    Container configuration for this Azure Function is stored in `"./config/config.yml"` file.
    But this path can be overridden by `CONFIG_PATH` environment variable.
    
    Note: This component has been deprecated. Use Azure FunctionService instead.
    
    ### References ###
        - `*:logger:*:*:1.0`:            (optional) :class:`ILogger <pip_services3_components.log.ILogger.ILogger>`  components to pass log messages
        - `*:counters:*:*:1.0`:          (optional) :class:`ICounters <pip_services3_components.count.ICounters.ICounters>`  components to pass collected measurements
        - `*:service:azure-function:*:1.0`: (optional) :class:`IAzureFunctionService <pip_services3_azure.services.IAzureFunctionService.IAzureFunctionService>` services to handle action requests
        - `*:service:commandable-azure-function:*:1.0`: (optional) :class:`IAzureFunctionService <pip_services3_azure.services.IAzureFunctionService.IAzureFunctionService>` services to handle action requests

    Example:

    .. code-block:: python
        class MyAzureFunctionFunction(CommandableAzureFunction):
            def __init__(self):
                super().__init__("mygroup", "MyGroup AzureFunction")
                self._dependency_resolver.put("controller", Descriptor("mygroup", "controller", "*", "*", "1.0"))
                
        azure_function = MyAzureFunctionFunction()
        service.run()
        print("MyAzureFunction is started")
    """

    def __init__(self, name: Optional[str], description: Optional[str]):
        """
        Creates a new instance of this Azure Function.

        :param name: (optional) a container name (accessible via ContextInfo)
        :param description: (optional) a container description (accessible via ContextInfo)
        """
        super().__init__(name, description)
        self._dependency_resolver.put('controller', 'none')

    def _get_parameters(self, context: func.HttpRequest) -> Parameters:
        """
        Returns body from Azure Function context.
        This method can be overloaded in child classes

        :param context: Azure Function context
        :return: Returns Parameters from context
        """
        return AzureFunctionContextHelper.get_parameters(context)

    def __register_command_set(self, command_set: CommandSet):
        commands = command_set.get_commands()
        for i in range(len(commands)):
            command = commands[i]

            def wrapper(command: ICommand):
                # wrapper for passing context
                def action(context: func.HttpRequest):
                    correlation_id = self._get_correlation_id(context)
                    args = self._get_parameters(context)
                    timing: InstrumentTiming = self._instrument(correlation_id,
                                                                self._info.name + '.' + command.get_name())

                    try:
                        result = command.execute(correlation_id, args)
                        timing.end_timing()
                        return result
                    except Exception as e:
                        timing.end_failure(e)
                        return func.HttpResponse(
                            body=JsonConverter.to_json(e),
                            status_code=400
                        )
                    finally:
                        timing.end_timing()

                return action

            self._register_action(command.get_name(), None, wrapper(command))

    def register(self):
        """
        Registers all actions in this Azure Function.
        """
        controller: ICommandable = self._dependency_resolver.get_one_required('controller')
        command_set = controller.get_command_set()
        self.__register_command_set(command_set)
