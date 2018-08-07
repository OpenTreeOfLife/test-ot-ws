#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import jsonschema
from otwstest import compose_schema2version, SCHEMA_URL_PREF
from otwstest.schema.tree_of_life.about import (get_v3_taxon_props_dict,
                                                get_v3_tol_taxon_props_dict)


def get_tree_of_life_mrca_properties(version):
    if version == 'v2':
        v = {}
        str_props = ["mrca_rank", "mrca_name", "tree_id",
                     "ott_id", "mrca_unique_name", "nearest_taxon_mrca_unique_name",
                     "nearest_taxon_mrca_name", "nearest_taxon_mrca_rank", ]
        int_props = ["nearest_taxon_mrca_node_id", "nearest_taxon_mrca_ott_id",
                     "mrca_node_id"]
        list_props = ["invalid_node_ids", "node_ids_not_in_tree",
                      "ott_ids_not_in_tree", "invalid_ott_ids"]
        for p in str_props:
            v[p] = {"type": "string"}
        for p in int_props:
            v[p] = {"type": "integer"}
        for p in list_props:
            v[p] = {"type": "array"}
    else:

        mrca = {
            "partial_path_of": {"type": "object"},
            "supported_by": {"type": "object"},
            "terminal": {"type": "object"},
        }
        mrca.update(get_v3_taxon_props_dict())
        v = {
            "mrca": mrca,
            "nearest_taxon": {"type": "object",
                              "properties": get_v3_tol_taxon_props_dict()},
            "source_id_map": {"type": "object"},
        }
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
        "properties": get_tree_of_life_mrca_properties('v3'),
        "required": ["mrca", "source_id_map"]
    }
    v2 = copy.deepcopy(current)
    p2 = get_tree_of_life_mrca_properties('v2')
    v2["properties"] = p2
    v2["required"] = list(p2.keys())
    _version2schema = compose_schema2version(v2=v2, current=current)
    return get_version2schema()


def schema_for_version(version):
    return get_version2schema()[version]


def validate(doc, version='current'):
    jsonschema.validate(doc, schema_for_version(version))
    return True
