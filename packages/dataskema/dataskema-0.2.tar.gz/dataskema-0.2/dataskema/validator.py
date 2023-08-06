# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring, C0301
"""
Validador
"""
import re


def _trim(string: str):
    if string is None:
        return ''
    if not isinstance(string, str):
        string = str(string)
    return string.strip(' \t\r\n')


class ValidationError(ValueError):
    """
    Error de validación
    """
    def __init__(self, message: str, errors: dict):
        self.errors = errors
        super(ValidationError, self).__init__(message)

    def get_error_msgs(self) -> list:
        text_list = []
        for field, value in self.errors.items():
            if field is None:
                continue
            is_valid = value.get('valid')
            if is_valid is True:
                continue
            message = value.get('message')
            text_list.append(field + ': ' + message)
        return text_list


class Validator:

    def __init__(self, message_prefix: str or None = None):
        self.checks = {}
        self.message_prefix = message_prefix

    def clear(self):
        self.checks.clear()

    def get_errors(self, separator: str) -> str:
        text = ''
        for field, value in self.checks.items():
            if field is None:
                continue
            is_valid = value.get('valid')
            if is_valid is True:
                continue
            message = value.get('message')
            if text != '':
                text = text + separator
            text = text + field + ': ' + message
        return text

    def get_error(self, pname: str) -> dict:
        return self.checks.get(pname)

    @staticmethod
    def add_row_error_list(error_list: list, row: int, error: str):
        error_list.append('[Row: ' + str(row) + '] ' + error)

    @staticmethod
    def add_line_error_list(error_list: list, line: int, error: str):
        error_list.append('[Line: ' + str(line) + '] ' + error)

    def dump_row_error_list(self, error_list: list, row: int):
        self.dump_error_list(error_list, '[Row: ' + str(row) + '] ')

    def dump_line_error_list(self, error_list: list, line: int):
        self.dump_error_list(error_list, '[Line: ' + str(line) + '] ')

    def dump_error_list(self, error_list: list, extra: str = ''):
        if len(self.checks) > 0:
            for field, value in self.checks.items():
                if field is None:
                    continue
                is_valid = value.get('valid')
                if is_valid is True:
                    continue
                message = value.get('message')
                if message is None:
                    continue
                error_list.append(extra + field + ': ' + message)
            self.checks.clear()

    def has_errors(self) -> bool:
        total = 0
        for value in self.checks.values():
            is_valid = value.get('valid')
            if not is_valid or is_valid is False:
                total = total + 1
        return total

    def add_field(self, pname: str):
        self.checks[pname] = {'valid': True}

    def add_message(self, pname: str, error: str):
        if self.message_prefix is not None:
            error = self.message_prefix + ': ' + error
        self.checks[pname] = {'message': error, 'valid': False}

    def raise_validation_error(self):
        if len(self.checks) > 0:
            for field, check in self.checks.items():
                is_valid = check.get('valid')
                if is_valid:
                    continue
                message = check.get('message')
                raise ValidationError(message, self.checks)

    def check_mandatory(self, pname: str, pvalue: str) -> bool:
        """
        Comprueba que el parámetro 'pname' está definido y no es una cadena vacía. Lanza una excepción si no valida
        :param self:
        :param pname: nombre del parámetro
        :param pvalue: valor del parámetro
        """
        if pvalue is None or (isinstance(pvalue, str) and len(_trim(pvalue)) == 0):
            self.add_message(pname, "Field required")
            return False
        self.add_field(pname)
        return True

    def check_regexp(self, pname: str, pvalue: str, pattern_to_match: str, message: str or None) -> bool:
        """
        Comprueba que el parámetro 'pname' valida una expresión regular. Lanza una excepción si no valida
        :param self:
        :param pname: nombre del parámetro
        :param pvalue: valor del parámetro
        :param pattern_to_match: la expresión regular a validar en el parámetro
        :param message: Mensaje a incluir en caso de error
        """
        if pvalue is not None and len(_trim(pvalue)) > 0:
            regex = re.compile(pattern_to_match, re.I)
            match = regex.match(str(pvalue))
            if not bool(match):
                if not message:
                    message = "Invalid format"
                self.add_message(pname, message)
                return False
            self.add_field(pname)
        return True

    def check_minsize(self, pname: str, pvalue: str, minvalue: int or None) -> bool:
        """
        Comprueba que el parámetro 'pname' valida un tamaño máximo en su valor
        :param self:
        :param pname: nombre del parámetro
        :param pvalue: valor del parámetro
        :param minvalue: tamaño mínimo
        """
        slen = len(_trim(pvalue))
        if pvalue is not None and minvalue is not None and slen < minvalue:
            self.add_message(pname, f"Value too short (min. {str(minvalue)})")
            return False
        self.add_field(pname)
        return True

    def check_maxsize(self, pname: str, pvalue: str, maxvalue: int or None) -> bool:
        """
        Comprueba que el parámetro 'pname' valida un tamaño máximo en su valor
        :param self:
        :param pname: nombre del parámetro
        :param pvalue: valor del parámetro
        :param maxvalue: tamaño máximo
        """
        slen = len(_trim(pvalue))
        if pvalue is not None and maxvalue is not None and slen > maxvalue:
            self.add_message(pname, f"Value too large (max. {str(maxvalue)})")
            return False
        self.add_field(pname)
        return True

    def _add_field_and_trim_value(self, pname: str, pvalue: str or None) -> str:
        if pvalue is not None and isinstance(pvalue, str):
            pvalue = _trim(pvalue)
            if len(pvalue) > 0:
                self.add_field(pname)
        return pvalue

    def check_obj(self, pname: str, pvalue: any, mandatory: bool = False) -> any or None:
        if mandatory and not self.check_mandatory(pname, pvalue):
            return None
        return pvalue

    def check_str(self, pname: str, pvalue: str, minsize: int or None, maxsize: int or None,
                  mandatory: bool) -> str or None:
        if mandatory and not self.check_mandatory(pname, pvalue):
            return None
        if pvalue is not None and isinstance(pvalue, list):
            return pvalue
        if pvalue is None or not isinstance(pvalue, str):
            return None
        if not self.check_minsize(pname, pvalue, minsize):
            return None
        if not self.check_maxsize(pname, pvalue, maxsize):
            return None
        return self._add_field_and_trim_value(pname, pvalue)

    def check_int(self, pname: str, pvalue: str, mandatory: bool) -> int or None:
        """
        Comprueba que el parámetro 'pname' valida un número entero
        :param self:
        :param pname: nombre del parámetro
        :param pvalue: valor del parámetro
        :param mandatory: si es mandatorio
        """
        self.add_field(pname)
        if mandatory and not self.check_mandatory(pname, pvalue):
            return None
        if isinstance(pvalue, int):
            return pvalue
        if isinstance(pvalue, float):
            return int(pvalue)
        if not isinstance(pvalue, str):
            return None
        pvalue = _trim(pvalue)
        if pvalue is None or pvalue == '':
            return None
        if not self.check_maxsize(pname, pvalue, 50):
            return None
        if not self.check_regexp(pname, pvalue, '^\\d+$', "Invalid integer number"):
            return None
        return int(self._add_field_and_trim_value(pname, pvalue))

    def check_int_with_range(self, pname: str, pvalue: str, vmin: int or None, vmax: int or None,
                             mandatory: bool) -> int or None:
        """
        Comprueba que el parámetro 'pname' valida un número entero
        :param self:
        :param pname: nombre del parámetro
        :param pvalue: valor del parámetro
        :param vmin: valor mínimo del parámetro o None si no hay límite
        :param vmax: valor máximo del parámetro o None si no hay límite
        :param mandatory: si es mandatorio
        """
        value = self.check_int(pname, pvalue, mandatory)
        if value is None:
            return None
        if (vmin is not None and value < vmin) or (vmax is not None and value > vmax):
            self.add_message(pname, f'Numeric value out of range ({vmin} - {vmax})')
            return None
        return value

    def check_bool(self, pname: str, pvalue: str) -> bool:
        """
        Comprueba que el parámetro 'pname' sea un booleano de cadena 'true' o 'false'

        :param self:
        :param pname: nombre del parámetro
        :param pvalue: valor del parámetro
        """
        if pvalue is None:
            return False
        if isinstance(pvalue, bool):
            return pvalue
        if self.check_whitelist(pname, pvalue, ['true', 'false'], False) and pvalue == 'true':
            self.add_field(pname)
            return True
        return False

    def check_whitelist(self, pname: str, pvalue: str, whitelist: [], mandatory: bool) -> str or None:
        """
        Comprueba que el parámetro 'pname' se encuentre en una whitelist

        :param self:
        :param pname: nombre del parámetro
        :param pvalue: valor del parámetro
        :param whitelist: lista de valores admitidos
        :param mandatory: si es mandatorio

        :return: si verifica o no
        """
        if mandatory and not self.check_mandatory(pname, pvalue):
            return None
        if isinstance(pvalue, str):
            if pvalue is None or _trim(pvalue) == '':
                return None
            for item in whitelist:
                if item == pvalue:
                    return item
            self.invalid_value(pname)
        return None

    def invalid_value(self, pname: str):
        """
        Lanza una excepción genérica de falta de validación
        :param self:
        :param pname: nombre del parámetro
        """
        self.add_field(pname)
        self.add_message(pname, "Invalid param value")
