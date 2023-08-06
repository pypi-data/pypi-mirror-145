# -*- coding: utf-8 -*-
from pip_services3_commons.config import ConfigParams

from pip_services3_azure.connect.AzureConnectionParams import AzureConnectionParams
from pip_services3_azure.connect.AzureConnectionResolver import AzureConnectionResolver


class TestAzureConnectionParams:

    def test_empty_connection(self):
        connection = AzureConnectionParams()

        assert connection.get_function_uri() is None
        assert connection.get_app_name() is None
        assert connection.get_function_name() is None
        assert connection.get_auth_code() is None
        assert connection.get_protocol() is None

    def test_compose_config(self):
        config1 = ConfigParams.from_tuples(
            'connection.uri', 'http://myapp.azurewebsites.net/api/myfunction',
            'credential.auth_code', '1234',
        )

        config2 = ConfigParams.from_tuples(
            'connection.protocol', 'http',
            'connection.app_name', 'myapp',
            'connection.function_name', 'myfunction',
            'credential.auth_code', '1234',
        )

        resolver = AzureConnectionResolver()
        resolver.configure(config1)
        connection = resolver.resolve('')

        assert 'http://myapp.azurewebsites.net/api/myfunction' == connection.get_function_uri()
        assert 'myapp' == connection.get_app_name()
        assert 'http' == connection.get_protocol()
        assert 'myfunction' == connection.get_function_name()
        assert '1234' == connection.get_auth_code()

        resolver = AzureConnectionResolver()
        resolver.configure(config2)
        connection = resolver.resolve('')

        assert 'http://myapp.azurewebsites.net/api/myfunction' == connection.get_function_uri()
        assert 'http' == connection.get_protocol()
        assert 'myapp' == connection.get_app_name()
        assert 'myfunction' == connection.get_function_name()
        assert '1234' == connection.get_auth_code()
