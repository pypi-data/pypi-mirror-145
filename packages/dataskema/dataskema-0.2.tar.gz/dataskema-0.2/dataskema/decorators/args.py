# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring, C0301
import functools
from dataskema.data_schema import Args


def args(**kwargs):
    def inner_function(function):
        @functools.wraps(function)
        def wrapper(**kwargs2):
            args_validator = Args(kwargs2)
            outdata = args_validator.check_schema(kwargs)
            outdata.update(kwargs2)
            print("decorator args: " + str(outdata))
            return function(**outdata)
        return wrapper
    return inner_function
