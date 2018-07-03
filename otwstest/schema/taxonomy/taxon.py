#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import jsonschema


def taxon_obj_properties(version):
    p = {
        "flags": {
            "type": "array",
            "items": {"type": "string"}
        },
        "rank": {"type": "string"},
        "synonyms": {
            "type": "array",
            "items": {"type": "string"}
        },
        "tax_sources": {
            "type": "array",
            "items": {"type": "string"}
        },
        "unique_name": {"type": "string"}
    }
    if version == 'v2':
        p["node_id"] = {"type": "integer"}
        p["ot:ottId"] = {"type": "integer"}
        p["ot:ottTaxonName"] = {"type": "string"}
    else:
        p["ott_id"] = {"type": "integer"}
        p["name"] = {"type": "string"}
        p["is_suppressed"] = {"type": "boolean"}
    return p


current = {
    "$id": "https://tree.opentreeoflife.org/schema/current/taxonomy/taxon.json",
    "type": "object",
    "definitions": {},
    "$schema": "http://json-schema.org/draft-07/schema#"
}

v2 = copy.deepcopy(current)
v2['properties'] = taxon_obj_properties('v2')
current['properties'] = taxon_obj_properties('v3')
v3 = copy.deepcopy(current)
v3['$id'] = v3['$id'].replace('/current/', '/v3/')
v2['$id'] = v2['$id'].replace('/current/', '/v3/')

_version2schema = {'current': current, 'v2': v2, 'v3': v3}


def validate(doc, version='current'):
    schema = _version2schema[version]
    jsonschema.validate(doc, schema)
    return True
