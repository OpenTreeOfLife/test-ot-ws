#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import jsonschema
from otwstest import compose_schema2version, SCHEMA_URL_PREF


def get_tree_of_life_induced_subtree_properties(version):
    r = {
        "newick": {"type": "string"},
    }
    if version == 'v2':
        v = {
            "node_ids_not_in_graph": {
                "type": "array",
                "items": {"type": "integer"}
            },
            "node_ids_not_in_tree": {
                "type": "array",
                "items": {"type": "integer"}
            },
            "ott_ids_not_in_graph":  {
                "type": "array",
                "items": {"type": "integer"}
            },
            "ott_ids_not_in_tree":  {
                "type": "array",
                "items": {"type": "integer"}
            },
            "tree_id": {"type": "string"}
        }
    else:
        v = {
            "supporting_studies": {
                "type": "array",
                "items": {"type": "string"}
            }
        }
    r.update(v)
    return r

_version2schema = None


def get_version2schema():
    global _version2schema
    if _version2schema is not None:
        return _version2schema
    p3 = get_tree_of_life_induced_subtree_properties('v3')
    current = {
        "$id": SCHEMA_URL_PREF + "current/tree_of_life/about.json",
        "type": "object",
        "$schema": "http://json-schema.org/draft-07/schema#",
        "properties": p3,
        "required": list(p3.keys())
    }
    v2 = copy.deepcopy(current)
    p2 = get_tree_of_life_induced_subtree_properties('v2')
    v2["properties"] = p2
    v2["required"] = list(p2.keys())
    _version2schema = compose_schema2version(v2=v2, current=current)
    return get_version2schema()


def schema_for_version(version):
    return get_version2schema()[version]


def validate(doc, version='current'):
    jsonschema.validate(doc, schema_for_version(version))
    return True
