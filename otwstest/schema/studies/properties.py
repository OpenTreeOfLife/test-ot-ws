#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import jsonschema
from otwstest import compose_schema2version, SCHEMA_URL_PREF
from otwstest.schema.tree_of_life.about import (get_v3_taxon_props_dict,
                                                get_v3_tol_taxon_props_dict)
from otwstest.schema.primitives import array_of_strings

def get_find_properties_properties(version):
    return {
        "tree_properties": array_of_strings,
        "study_properties": array_of_strings,
    }

_version2schema = None


def get_version2schema():
    global _version2schema
    if _version2schema is not None:
        return _version2schema
    current = {
        "$id": SCHEMA_URL_PREF + "current/tree_of_life/about.json",
        "type": "object",
        "$schema": "http://json-schema.org/draft-07/schema#",
        "properties": get_find_properties_properties('v3'),
        "required": ["tree_properties", "study_properties"]
    }
    v2 = copy.deepcopy(current)
    _version2schema = compose_schema2version(v2=v2, current=current)
    return get_version2schema()


def schema_for_version(version):
    return get_version2schema()[version]


def validate(doc, version='current'):
    jsonschema.validate(doc, schema_for_version(version))
    return True
