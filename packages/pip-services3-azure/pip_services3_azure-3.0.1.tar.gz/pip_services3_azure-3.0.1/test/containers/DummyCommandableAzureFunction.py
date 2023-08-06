# -*- coding: utf-8 -*-
from pip_services3_commons.refer import Descriptor

from pip_services3_azure.containers import CommandableAzureFunction
from test.DummyFactory import DummyFactory


class DummyCommandableAzureFunction(CommandableAzureFunction):
    def __init__(self):
        super(DummyCommandableAzureFunction, self).__init__("dummy", "Dummy Azure function")
        self._dependency_resolver.put('controller',
                                      Descriptor('pip-services-dummies', 'controller', 'default', '*', '*'))
        self._factories.add(DummyFactory())


handler = DummyCommandableAzureFunction().get_handler()
