#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy

import jsonschema

from otwstest import compose_schema2version, SCHEMA_URL_PREF

_version2schema = None


def get_version2schema():
    global _version2schema
    if _version2schema is not None:
        return _version2schema
    current = {
        "$id": SCHEMA_URL_PREF + "current/tree_of_life/about.json",
        "type": "object",
        "$schema": "http://json-schema.org/draft-07/schema#",
        "properties": {
            "newick": {"type": "string"},
        },
        "required": ["newick"]
    }
    v2 = copy.deepcopy(current)
    p2 = v2["properties"]
    p2["tree_id"] = {"type": "string"}
    v2["required"] = list(p2.keys())
    _version2schema = compose_schema2version(v2=v2, current=current)
    return get_version2schema()


def schema_for_version(version):
    return get_version2schema()[version]


def validate(doc, version='current'):
    jsonschema.validate(doc, schema_for_version(version))
    return True
