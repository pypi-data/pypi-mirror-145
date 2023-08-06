# -*- coding: utf-8 -*-
from typing import Optional

from pip_services3_commons.data import FilterParams, PagingParams, DataPage

from pip_services3_azure.clients import CommandableAzureFunctionClient
from test.Dummy import Dummy
from test.IDummyClient import IDummyClient


class DummyCommandableAzureFunctionClient(CommandableAzureFunctionClient, IDummyClient):

    def __init__(self):
        super().__init__('dummies')

    def get_dummies(self, correlation_id: Optional[str], filter: FilterParams, paging: PagingParams) -> DataPage:
        response = self.call_command('get_dummies', correlation_id, {'filter': filter, 'paging': paging.to_json()})

        items = []
        for item in response['data']:
            items.append(Dummy(**item))
        return DataPage(items)

    def get_dummy_by_id(self, correlation_id: Optional[str], id: str) -> Optional[Dummy]:
        response = self.call_command('get_dummy_by_id', correlation_id, {'dummy_id': id})

        if not response:
            return None

        return Dummy(**response)

    def create_dummy(self, correlation_id: Optional[str], entity: Dummy) -> Dummy:
        response = self.call_command('create_dummy', correlation_id, {'dummy': entity.to_dict()})
        return Dummy(**response)

    def update_dummy(self, correlation_id: Optional[str], entity: Dummy) -> Dummy:
        response = self.call_command('update_dummy', correlation_id, {'dummy': entity.to_dict()})

        return Dummy(**response)

    def delete__dummy(self, correlation_id: Optional[str], id: str) -> Dummy:
        response = self.call_command('delete_dummy', correlation_id, {'dummy_id': id})

        return Dummy(**response)
