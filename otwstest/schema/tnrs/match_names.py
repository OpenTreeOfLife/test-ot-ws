#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import jsonschema
from otwstest.schema.taxonomy.about import get_taxonomy_about_properties
from otwstest import compose_schema2version


def get_match_names_match_objects(version):
    return {
        "type": "object",
        "properties": {
            "flags": {"type": "array", "items": {"type": "string"}},
            "is_approximate_match": {"type": "boolean"},
            "is_deprecated": {"type": "boolean"},
            "is_dubious": {"type": "boolean"},
            "is_synonym": {"type": "boolean"},
            "matched_name": {"type": "string"},
            "matched_node_id": {"type": "integer"},
            "nomenclature_code": {"type": "string"},
            "ot:ottId": {"type": "integer"},
            "ot:ottTaxonName": {"type": "string"},
            "rank": {"type": "string"},
            "score": {"type": "number"},
            "search_string": {"type": "string"},
            "synonyms": {"type": "array", "items": {"type": "string"}},
            "tax_sources": {"type": "array", "items": {"type": "string"}},
            "unique_name": {"type": "string"},
        }
    }


def get_match_names_results_objects(version):
    return {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "matches": {"type": "array",
                        "items": get_match_names_match_objects(version)}
        }
    }


_version2schema = None


def get_version2schema():
    global _version2schema
    if _version2schema is not None:
        return _version2schema
    current = {
        "$id": "https://tree.opentreeoflife.org/schema/current/tnrs/infer_context.json",
        "type": "object",
        "$schema": "http://json-schema.org/draft-07/schema#",
        "properties": {
            "context": {"type": "string"},
            "governing_code": {"type": "string"},
            "includes_approximate_matches": {"type": "boolean"},
            "includes_deprecated_taxa": {"type": "boolean"},
            "includes_dubious_names": {"type": "boolean"},
            "matched_name_ids": {"type": "array",
                                 "items": {"type": "string"}
                                 },
            "results": {"type": "array", "items": get_match_names_results_objects('v2')},
            "taxonomy": get_taxonomy_about_properties('v2'),
            "unambiguous_name_ids": {"type": "array",
                                     "items": {"type": "string"}
                                     },
            "unmatched_name_ids": {"type": "array",
                                   "items": {"type": "string"}
                                   }
        },
        "required": ["context", "governing_code", "includes_approximate_matches",
                     "includes_deprecated_taxa", "matched_name_ids", "results",
                     "taxonomy", "unambiguous_name_ids", "unmatched_name_ids"]
    }

    v2 = copy.deepcopy(current)
    v2['$id'] = v2['$id'].replace('/current/', '/v3/')
    _version2schema = compose_schema2version(v2=v2, current=current)
    return _version2schema


def schema_for_version(version):
    return get_version2schema()[version]


def validate(doc, version='current'):
    jsonschema.validate(doc, schema_for_version(version))
    return True
