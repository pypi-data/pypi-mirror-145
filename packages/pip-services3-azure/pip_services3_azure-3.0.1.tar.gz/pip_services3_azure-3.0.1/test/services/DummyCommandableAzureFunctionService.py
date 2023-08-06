# -*- coding: utf-8 -*-
from pip_services3_commons.refer import Descriptor

from pip_services3_azure.services import CommandableAzureFunctionService


class DummyCommandableAzureFunctionService(CommandableAzureFunctionService):

    def __init__(self):
        super(DummyCommandableAzureFunctionService, self).__init__('dummies')
        self._dependency_resolver.put('controller',
                                      Descriptor('pip-services-dummies', 'controller', 'default', '*', '*'))
