#!/usr/bin/env python
# -*- coding: utf-8 -*-


# noinspection PyPep8Naming
def SCHEMA_STRING():
    return {"type": "string"}


# noinspection PyPep8Naming
def SCHEMA_INTEGER():
    return {"type": "integer"}


# noinspection PyPep8Naming
def SCHEMA_BOOL():
    return {"type": "boolean"}


# noinspection PyPep8Naming
def SCHEMA_OBJECT():
    return {"type": "object"}


# noinspection PyPep8Naming
def SCHEMA_ARRAY_OF_STRINGS():
    return {"type": "array", "items": SCHEMA_STRING()}


# noinspection PyPep8Naming
def SCHEMA_ARRAY():
    return {"type": "array"}


# noinspection PyPep8Naming
def SCHEMA_ARRAY_OBJECTS():
    return {"type": "array", "items": SCHEMA_OBJECT()}
