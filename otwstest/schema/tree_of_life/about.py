#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import jsonschema
from otwstest import compose_schema2version, SCHEMA_URL_PREF


def get_tree_of_life_about_properties(version):
    r = {"num_source_studies": {"type": "integer"}, }
    if version == 'v2':
        v = {
            "date": {"type": "string"},
            "num_tips": {"type": "integer"},
            "root_node_id": {"type": "integer"},
            "root_ott_id": {"type": "integer"},
            "root_taxon_name": {"type": "string"},
            "study_list": {
                "type": "array",
                "items": {"type": "object"}
            },
            "taxonomy_version": {"type": "string"},
            "tree_id": {"type": "string"},
        }
    else:
        v = {
            "date_created": {"type": "string"},
            "filtered_flags": {
                "type": "array",
                "items": {"type": "string"}
            },
            "source_list": {
                "type": "array",
                "items": {"type": "string"}
            },
            "taxonomy": {"type": "string"},
            "num_source_trees": {"type": "integer"},
            "source_id_map": {"type": "object"},
            "synth_id": {"type": "string"},
            "root": {
                "type": "object",
                "properties": {
                    "taxon": {
                        "type": "object",
                        "properties": {
                            "tax_sources": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "ott_id": {"type": "integer"},
                            "rank": {"type": "string"},
                            "name": {"type": "string"},
                            "unique_name": {"type": "string"}
                        }
                    },
                    "num_tips": {"type": "integer"},
                    "node_id": {"type": "string"}
                }
            }
        }
    r.update(v)
    return r


_version2schema = None


def get_version2schema():
    global _version2schema
    if _version2schema is not None:
        return _version2schema
    current = {
        "$id": SCHEMA_URL_PREF + "current/tree_of_life/about.json",
        "type": "object",
        "$schema": "http://json-schema.org/draft-07/schema#",
        "properties": get_tree_of_life_about_properties('v3'),
        "required": ["date_created", "num_source_studies", "num_source_trees",
                     "root", "synth_id", "taxonomy"]
    }
    v2 = copy.deepcopy(current)
    p2 = get_tree_of_life_about_properties('v2')
    v2["properties"] = p2
    v2["required"] = list(p2.keys())
    _version2schema = compose_schema2version(v2=v2, current=current)
    return get_version2schema()


def schema_for_version(version):
    return get_version2schema()[version]


def validate(doc, version='current'):
    jsonschema.validate(doc, schema_for_version(version))
    return True
