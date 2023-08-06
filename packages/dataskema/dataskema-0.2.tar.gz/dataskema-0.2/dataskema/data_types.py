# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring, C0301

class DataTypes:

    generic = {
        'type': 'any',
    }
    boolean = {
        'type': 'bool',
    }
    integer = {
        'type': 'int',
    }
    positive = {
        'type': 'int',
        'min-value': 1,
    }
    negative = {
        'type': 'int',
        'min-value': -1,
    }
    zero_positive = {
        'type': 'int',
        'min-value': 0,
    }
    zero_negative = {
        'type': 'int',
        'max-value': 0,
    }
    decimal = {
        'type': 'float',
    }
    hexadecimal = {
        'regexp': '^[A-Fa-f0-9]+$',
    }
    alfanumeric = {
        'regexp': '^[A-Za-z0-9]+$',
    }
    short_id = {
        'max-size': 20,
    }
    long_id = {
        'max-size': 40,
    }
    short_name = {
        'max-size': 50,
    }
    name = {
        'max-size': 100,
    }
    title = {
        'max-size': 200,
    }
    summary = {
        'max-size': 2000,
    }
    text = {
        'max-size': 500000,
    }
    version = {
        'regexp': '^[a-zA-Z0-9\\.\\-\\+]+$',
    }
    search = {
        'max-size': 50,
    }
    email = {
        'regexp': '^[a-zA-Z0-9_+&*-]+(?:\\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,7}$',
        'max-size': 100,
    }
    url = {
        'regexp': '^((((https?|ftps?|gopher|telnet|nntp)://)|(mailto:|news:))(%[0-9A-Fa-f]{2}|[-()_.!~*\';/?:@&'
                  '=+$,A-Za-z0-9])+)([).!\';/?:,][[:blank:|:blank:]])?$',
        'max-size': 500,
    }
    basic_password = {
        'regexp': '^[a-zA-Z0-9_+&*\\-_\\(\\)]+$',
        'max-size': 50,
    }

    @staticmethod
    def type(ptype: dict, ptyp2: dict) -> dict:
        ptype = dict(ptype)
        ptype.update(ptyp2)
        return ptype

    @staticmethod
    def mandatory(ptype: dict) -> dict:
        return DataTypes.type(ptype, {'mandatory': True})

    @staticmethod
    def lower(ptype: dict) -> dict:
        return DataTypes.type(ptype, {'to': 'lower'})

    @staticmethod
    def upper(ptype: dict) -> dict:
        return DataTypes.type(ptype, {'to': 'upper'})

    @staticmethod
    def default(ptype: dict, value: any) -> dict:
        return DataTypes.type(ptype, {'default': value})

    @staticmethod
    def label(ptype: dict, label: str) -> dict:
        return DataTypes.type(ptype, {'label': label})
