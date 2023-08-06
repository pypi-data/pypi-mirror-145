# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring, C0301
import functools
from dataskema.data_schema import DataSchema
from flask import request


class JSON(DataSchema):
    def __init__(self):
        super(JSON, self).__init__(request.get_json())


class Query(DataSchema):
    def __init__(self):
        super(Query, self).__init__(request.args)


def json(**kwargs):
    def inner_function(function):
        @functools.wraps(function)
        def wrapper(**data):
            json_validator = JSON()
            outdata = json_validator.check_schema(kwargs)
            outdata.update(data)
            print("decorator json: " + str(outdata))
            return function(**outdata)
        return wrapper
    return inner_function


def query(**kwargs):
    def inner_function(function):
        @functools.wraps(function)
        def wrapper(**data):
            query_validator = Query()
            outdata = query_validator.check_schema(kwargs)
            outdata.update(data)
            print("decorator query: " + str(outdata))
            return function(**outdata)
        return wrapper
    return inner_function
