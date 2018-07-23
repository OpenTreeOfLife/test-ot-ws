#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import jsonschema
from otwstest import compose_schema2version, SCHEMA_URL_PREF


def get_tree_of_life_about_properties(version):
    if version == 'v2':
        return {
            "author": {"type": "string"},
            "name": {"type": "string"},
            "source": {"type": "string"},
            "version": {"type": "string"},
            "weburl": {"type": "string"}
        }
    return {
        "date_created": {"type": "string"},
        "filtered_flags": {
            "type": "array",
            "items": {"type": "string"}
        },
        "source_list": {
            "type": "array",
            "items": {"type": "string"}
        },
        "num_source_studies": {"type": "integer"},
        "num_source_trees": {"type": "integer"},
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
        },
        "taxonomy": {"type": "string"},
        "source_id_map": {"type": "object"},
        "synth_id": {"type": "string"}
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
        "properties": get_tree_of_life_about_properties('v3'),
        "required": ["date_created", "num_source_studies", "num_source_trees",
                     "root", "synth_id"]
    }
    _version2schema = compose_schema2version(v2=copy.deepcopy(current), current=current)
    return get_version2schema()


def schema_for_version(version):
    return get_version2schema()[version]


def validate(doc, version='current'):
    jsonschema.validate(doc, schema_for_version(version))
    return True
