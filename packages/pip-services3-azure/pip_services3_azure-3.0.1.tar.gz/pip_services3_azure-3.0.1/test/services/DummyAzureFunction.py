# -*- coding: utf-8 -*-
from typing import Callable, Any

import azure.functions as func

from pip_services3_azure.containers import AzureFunction
from test.DummyFactory import DummyFactory


class DummyAzureFunction(AzureFunction):
    def __init__(self):
        super().__init__("dummy", "Dummy Azure function")
        self._factories.add(DummyFactory())


handler: Callable[[func.HttpRequest], Any] = DummyAzureFunction().get_handler()
