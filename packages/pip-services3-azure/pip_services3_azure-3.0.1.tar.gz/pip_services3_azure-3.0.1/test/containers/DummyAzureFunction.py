# -*- coding: utf-8 -*-
import json
from copy import deepcopy

import azure.functions as func
from pip_services3_commons.convert import TypeCode
from pip_services3_commons.data import DataPage, FilterParams, PagingParams
from pip_services3_commons.refer import Descriptor, IReferences
from pip_services3_commons.validate import ObjectSchema, FilterParamsSchema, PagingParamsSchema

from pip_services3_azure.containers import AzureFunction
from test.Dummy import Dummy
from test.DummyFactory import DummyFactory
from test.DummySchema import DummySchema
from test.IDummyController import IDummyController


class DummyAzureFunction(AzureFunction):
    def __init__(self):
        super(DummyAzureFunction, self).__init__("dummy", "Dummy Azure function")
        self._dependency_resolver.put('controller',
                                      Descriptor('pip-services-dummies', 'controller', 'default', '*', '*'))
        self._factories.add(DummyFactory())

        self._controller: IDummyController = None

        self.__headers: dict = {'Content-Type': 'application/json'}

    def set_references(self, references: IReferences):
        super(DummyAzureFunction, self).set_references(references)
        self._controller = self._dependency_resolver.get_one_required('controller')

    def _get_body_data(self, context: func.HttpRequest) -> dict:
        params = deepcopy(context.get_body())

        if params:
            params = json.loads(params)
        return params

    def __get_page_by_filter(self, params: func.HttpRequest) -> func.HttpResponse:
        params = self._get_body_data(params)
        page = self._controller.get_page_by_filter(
            params.get('correlation_id'),
            FilterParams.from_value(params.get('filter')),
            PagingParams.from_value(params.get('paging'))
        )

        page.data = list(map(lambda d: json.dumps(d.to_dict()), page.data))
        return func.HttpResponse(body=json.dumps(page.to_json()), headers=self.__headers)

    def __get_one_by_id(self, params: func.HttpRequest) -> func.HttpResponse:
        params = self._get_body_data(params)
        dummy = self._controller.get_one_by_id(
            params.get('correlation_id'),
            params.get('dummy_id')
        )
        json_dummy = None if not dummy else json.dumps(dummy.to_dict())
        return func.HttpResponse(body=json_dummy, headers=self.__headers)

    def __create(self, params: func.HttpRequest) -> func.HttpResponse:
        params = self._get_body_data(params)
        dummy = self._controller.create(
            params.get('correlation_id'),
            Dummy(**params.get('dummy'))
        )
        return func.HttpResponse(body=json.dumps(dummy.to_dict()), headers=self.__headers)

    def __update(self, params: func.HttpRequest) -> func.HttpResponse:
        params = self._get_body_data(params)
        dummy = self._controller.update(
            params.get('correlation_id'),
            Dummy(**params.get('dummy'))
        )
        return func.HttpResponse(body=json.dumps(dummy.to_dict()), headers=self.__headers)

    def __delete_by_id(self, params: func.HttpRequest) -> func.HttpResponse:
        params = self._get_body_data(params)
        dummy = self._controller.delete_by_id(
            params.get('correlation_id'),
            params.get('dummy_id'),
        )
        return func.HttpResponse(body=json.dumps(dummy.to_dict()), headers=self.__headers)

    def register(self):
        self._register_action(
            'get_dummies',
            ObjectSchema(True).with_optional_property('body',ObjectSchema(True)
                    .with_optional_property("filter", FilterParamsSchema())
                    .with_optional_property("paging", PagingParamsSchema())),
            self.__get_page_by_filter
        )

        self._register_action(
            'get_dummy_by_id',
            ObjectSchema(True).with_optional_property("body", ObjectSchema(True)
                  .with_optional_property("dummy_id", TypeCode.String)),
            self.__get_one_by_id)

        self._register_action(
            'create_dummy',
            ObjectSchema(True).with_optional_property("body", ObjectSchema(True)
                    .with_required_property("dummy", DummySchema())),
            self.__create)

        self._register_action(
            'update_dummy',
            ObjectSchema(True).with_optional_property("body", ObjectSchema(True)
                    .with_optional_property("dummy", DummySchema())),
            self.__update)

        self._register_action(
            'delete_dummy',
            ObjectSchema(True).with_optional_property("body", ObjectSchema(True)
                    .with_optional_property("dummy_id", TypeCode.String)),
            self.__delete_by_id)
