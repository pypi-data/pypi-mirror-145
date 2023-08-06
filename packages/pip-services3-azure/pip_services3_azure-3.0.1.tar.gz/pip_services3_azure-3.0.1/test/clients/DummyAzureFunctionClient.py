# -*- coding: utf-8 -*-
import json
from typing import Optional

from pip_services3_commons.data import DataPage, PagingParams, FilterParams

from pip_services3_azure.clients.AzureFunctionClient import AzureFunctionClient
from test.Dummy import Dummy
from test.IDummyClient import IDummyClient


class DummyAzureFunctionClient(AzureFunctionClient, IDummyClient):

    def __init__(self):
        super().__init__()

    def get_dummies(self, correlation_id: Optional[str], filter: FilterParams, paging: PagingParams) -> DataPage:
        response = self._call('get_dummies', correlation_id, {'filter': filter, 'paging': paging.to_json()})
        items = []
        for item in response['data']:
            items.append(Dummy(**item))
        return DataPage(items)

    def get_dummy_by_id(self, correlation_id: Optional[str], id: str) -> Optional[Dummy]:
        response = self._call('get_dummy_by_id', correlation_id, {'dummy_id': id})

        if response is None or len(response) == 0:
            return

        return Dummy(**response)

    def create_dummy(self, correlation_id: Optional[str], entity: Dummy) -> Dummy:
        response = self._call('create_dummy', correlation_id, {'dummy': entity.to_dict()})

        return Dummy(**response)

    def update_dummy(self, correlation_id: Optional[str], entity: Dummy) -> Dummy:
        response = self._call('update_dummy', correlation_id, {'dummy': entity.to_dict()})

        return Dummy(**response)

    def delete__dummy(self, correlation_id: Optional[str], id: str) -> Dummy:
        response = self._call('delete_dummy', correlation_id, {'dummy_id': id})

        return Dummy(**response)
