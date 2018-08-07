#!/usr/bin/env python
# -*- coding: utf-8 -*-

SCHEMA_STRING = lambda: {"type": "string"}
SCHEMA_INTEGER = lambda: {"type": "integer"}
SCHEMA_BOOL = lambda: {"type": "boolean"}
SCHEMA_OBJECT = lambda: {"type": "object"}
SCHEMA_ARRAY_OF_STRINGS = lambda: {"type": "array", "items": SCHEMA_STRING()}
SCHEMA_ARRAY = lambda: {"type": "array"}
SCHEMA_ARRAY_OBJECTS = lambda: {"type": "array", "items": SCHEMA_OBJECT()}