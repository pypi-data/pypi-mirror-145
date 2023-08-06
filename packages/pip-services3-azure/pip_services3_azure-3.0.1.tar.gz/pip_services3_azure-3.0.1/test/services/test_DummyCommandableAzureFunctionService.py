# -*- coding: utf-8 -*-
from pip_services3_commons.config import ConfigParams

from test.containers.DummyCommandableAzureFunction import DummyCommandableAzureFunction
from test.services.DummyAzureFunctionServiceFixture import DummyAzureFunctionServiceFixture


class TestDummyCommandableAzureFunctionService:
    _function_service: DummyCommandableAzureFunction
    fixture: DummyAzureFunctionServiceFixture

    def setup_method(self):
        config = ConfigParams.from_tuples(
            'logger.descriptor', 'pip-services:logger:console:default:1.0',
            'controller.descriptor', 'pip-services-dummies:controller:default:default:1.0',
            'service.descriptor', 'pip-services-dummies:service:commandable-azure-function:default:1.0'
        )

        self._function_service = DummyCommandableAzureFunction()
        self._function_service.configure(config)
        self._function_service.open(None)

        self.fixture = DummyAzureFunctionServiceFixture(self._function_service)

    def teardown_method(self):
        self.fixture.teardown_method()

    def test_crud_operations(self):
        self.fixture.test_crud_operations()
