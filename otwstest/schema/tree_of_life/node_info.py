#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import jsonschema
from otwstest import compose_schema2version, SCHEMA_URL_PREF
from otwstest.schema.tree_of_life.about import (get_v3_taxon_props_dict,
                                                get_v3_tol_taxon_props_dict)

def get_tree_of_life_node_info_properties(version):
    if version == 'v2':
        v ={}
        str_props = ["tree_id",
                     "name", "rank", "tax_source", ]
        int_props = ["ott_id", 'num_synth_tips', 'num_tips', 'node_id']
        list_props =  ["tree_sources", 'synth_sources']
        for p in str_props:
            v[p] = {"type": "string"}
        for p in int_props:
            v[p] = {"type": "integer"}
        for p in list_props:
            v[p] = {"type": "array"}
        v['in_synth_tree'] = {"type": "boolean"}
    else:
        v = {
            "partial_path_of": {"type": "object"},
            "supported_by": {"type": "object"},
            "terminal": {"type": "object"},
        }
        v.update(get_v3_taxon_props_dict())
    return v


_version2schema = None


def get_version2schema():
    global _version2schema
    if _version2schema is not None:
        return _version2schema
    current = {
        "$id": SCHEMA_URL_PREF + "current/tree_of_life/about.json",
        "type": "object",
        "$schema": "http://json-schema.org/draft-07/schema#",
        "properties": get_tree_of_life_node_info_properties('v3'),
        "required": ['node_id', 'num_tips']
    }
    v2 = copy.deepcopy(current)
    p2 = get_tree_of_life_node_info_properties('v2')
    v2["properties"] = p2
    v2["required"] = list(p2.keys())
    _version2schema = compose_schema2version(v2=v2, current=current)
    return get_version2schema()


def schema_for_version(version):
    return get_version2schema()[version]


def validate(doc, version='current'):
    jsonschema.validate(doc, schema_for_version(version))
    return True
