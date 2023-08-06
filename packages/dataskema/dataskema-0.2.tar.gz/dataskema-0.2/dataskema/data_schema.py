# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring, C0301
from dataskema.validator import Validator

VALID_TYPES = ['str', 'int', 'list', 'bool', 'any']
VALID_TOS = ['lower', 'upper']

SCHEMA_MSG = "Parameter schema validation"


def _trim(string: str):
    if string is None:
        return ''
    if not isinstance(string, str):
        string = str(string)
    return string.strip(' \t\r\n')


def _log_value(value):
    value = str(value)
    if len(value) > 10:
        value = value[0:10] + '...'
    return value


def _typeof(value):
    stype = str(type(value))
    idx1 = stype.find("'")
    idx2 = stype.rfind("'")
    if idx2 <= idx1:
        raise RuntimeError(f"Type not found: {stype}")
    return stype[idx1 + 1:idx2]


class DataSchema:

    def __init__(self, data, message_prefix: str or None = None):
        self.data = dict(data) if data is not None and isinstance(data, dict) else {}
        self.validator = Validator(message_prefix)

    def __repr__(self):
        return str(self.data)

    def __to(self, name: str, func_name: str):
        value = self.get_obj(name)
        if isinstance(value, str):
            if func_name == 'lower':
                self.data[name] = value.lower()
            if func_name == 'upper':
                self.data[name] = value.upper()

    def __check_str(self, data_schema, name: str, mandatory: bool) -> any:
        white_list = data_schema.get_obj('white-list')
        if white_list is not None:
            return self.get_from_whitelist(name, white_list, mandatory)
        min_size = data_schema.get_int_with_range('min-size', 0, None, False)
        max_size = data_schema.get_int_with_range('max-size', 0, None, False)
        value = self.get_str(name, min_size, max_size, mandatory)
        regexp = data_schema.get_str('regexp', 0, None, False)
        if regexp is not None:
            logvalue = _log_value(value)
            self.validator.check_regexp(name, value, regexp, f"Invalid value '{logvalue}'")
        return value

    def __check_int(self, data_schema, name: str, mandatory: bool) -> any:
        min_val = data_schema.get_int('min-value', False)
        max_val = data_schema.get_int('max-value', False)
        return self.get_int_with_range(name, min_val, max_val, mandatory)

    def __check_bool(self,name: str) -> any:
        return self.get_bool(name)

    def __check_list(self, data_schema, name: str, mandatory: bool) -> any:
        separator = data_schema.get_str('separator', None, None, False)
        if separator is None:
            separator = ','
        min_size = data_schema.get_int_with_range('min-size', 0, None, False)
        max_size = data_schema.get_int_with_range('max-size', 0, None, False)
        value = self.get_str(name, min_size, max_size, mandatory)
        if value is not None:
            values = value.split(separator)
            itype = data_schema.get_obj('itype', True)
            iname = data_schema.get_str('iname', 0, 50, True)
            item_list = []
            for item in values:
                item = _trim(item)
                if len(item) == 0:
                    continue
                ival = Args(item)
                if itype is not None and isinstance(itype, dict):
                    ival.check_schema_item(iname, itype)
                ival.raise_validation_error()
                item_list.append(item)
            return item_list
        return None

    def __update_error_message(self, data_schema, name: str):
        error = self.validator.get_error(name)
        if error is not None:
            label = data_schema.get_str('label', 0, 50, False)
            if label is None:
                label = name
            msg = error.get('message')
            if msg is not None:
                error['message'] = label + ': ' + msg

    def check_schema_item(self, name: str, item: dict) -> any:
        data_schema = DataSchema(item, SCHEMA_MSG)
        itype = data_schema.get_from_whitelist('type', VALID_TYPES, False)
        if itype is None:
            itype = 'str'
        mandatory = data_schema.get_bool('mandatory')
        defvalue = data_schema.get_obj('default')
        if itype is None and defvalue is not None:
            def_itype = _typeof(defvalue)
            if itype != def_itype:
                data_schema.validator.add_message('default', f"Invalid param 'default' type '{def_itype}'")
        to = data_schema.get_from_whitelist('to', VALID_TOS, False)
        if to is not None:
            self.__to(name, to)
        value = None
        if itype == 'any':
            value = self.get_obj(name)
        elif itype == 'str':
            value = self.__check_str(data_schema, name, mandatory)
        elif itype == 'int':
            value = self.__check_int(data_schema, name, mandatory)
        elif itype == 'bool':
            value = self.__check_bool(name)
        elif itype == 'list':
            value = self.__check_list(data_schema, name, mandatory)
        else:
            data_schema.validator.add_message('type', f"Invalid 'type' value '{itype}'")
        if value is None and defvalue is not None:
            value = defvalue
            self.data[name] = value
        self.__update_error_message(data_schema, name)
        data_schema.raise_validation_error()
        return value

    def check_schema(self, schema: dict) -> dict:
        outdata = {}
        for (name, item) in schema.items():
            value = self.check_schema_item(name, item)
            outdata[name] = value
        self.raise_validation_error()
        return outdata

    def get_obj(self, pname: str, mandatory: bool = False) -> list or None:
        pvalue = self.data.get(pname)
        return self.validator.check_obj(pname, pvalue, mandatory)

    def get_str(self, pname: str, minsize: int or None, maxsize: int or None, mandatory: bool) -> str or None:
        pvalue = self.get_obj(pname)
        return self.validator.check_str(pname, pvalue, minsize, maxsize, mandatory)

    def get_int(self, pname: str, mandatory: bool) -> int or None:
        pvalue = self.get_obj(pname)
        return self.validator.check_int(pname, pvalue, mandatory)

    def get_int_with_range(self, pname: str, min_value: int or None, max_value: int or None,
                           mandatory: bool) -> int or None:
        pvalue = self.get_obj(pname)
        return self.validator.check_int_with_range(pname, pvalue, min_value, max_value, mandatory)

    def get_from_whitelist(self, pname: str, whitelist: list, mandatory: bool) -> str or None:
        pvalue = self.get_obj(pname)
        if not self.validator.check_whitelist(pname, pvalue, whitelist, mandatory):
            return None
        return pvalue

    def get_bool(self, pname: str) -> int or None:
        pvalue = self.get_obj(pname)
        return self.validator.check_bool(pname, pvalue)

    def get_validation(self) -> Validator:
        return self.validator

    def raise_validation_error(self):
        self.validator.raise_validation_error()


class Args(DataSchema):
    def __init__(self, params):
        super(Args, self).__init__(params)
