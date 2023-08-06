# -*- coding: utf-8 -*-
from pip_services3_commons.data import FilterParams, PagingParams

from test.Dummy import Dummy
from test.IDummyClient import IDummyClient


class DummyClientFixture:
    _client: IDummyClient

    def __init__(self, client: IDummyClient):
        self._client = client

    def test_crud_operations(self):
        dummy1 = Dummy(None, 'Key 1', 'Content 1')
        dummy2 = Dummy(None, 'Key 1', 'Content 1')

        # Create one dummy
        created_dummy1 = self._client.create_dummy(None, dummy1)
        assert created_dummy1 is not None
        assert created_dummy1.content == dummy1.content
        assert created_dummy1.key == dummy1.key

        dummy1 = created_dummy1

        # Create another dummy
        created_dummy2 = self._client.create_dummy(None, dummy2)
        assert created_dummy2 is not None
        assert created_dummy2 is not None
        assert created_dummy2.content == dummy2.content
        assert created_dummy2.key == dummy2.key

        # Get all dummies
        dummy_page = self._client.get_dummies(
            None,
            FilterParams(),
            PagingParams(0, 5, False)
        )

        assert dummy_page is not None
        assert len(dummy_page.data) >= 2

        # Update the dummy
        dummy1.content = 'Updated Content 1'
        updated_dummy1 = self._client.update_dummy(None, dummy1)
        assert updated_dummy1 is not None
        assert updated_dummy1.content == dummy1.content
        assert updated_dummy1.key == dummy1.key
        dummy1 = updated_dummy1

        # Delete dummy
        self._client.delete__dummy(None, dummy1.id)

        # Try to get delete dummy
        dummy = self._client.get_dummy_by_id(None, dummy1.id)

        assert dummy is None