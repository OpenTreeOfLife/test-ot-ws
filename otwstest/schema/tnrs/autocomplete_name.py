#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import jsonschema

current = {
    "$id": "https://tree.opentreeoflife.org/schema/current/tnrs/autocomplete_name.json",
    "type": "array",
    "$schema": "http://json-schema.org/draft-07/schema#",
    "items": {
        "type": "object"
    }
}


def add_taxon_properties(par, version):
    p = {
        "is_dubious": {"type": "boolean"},
        "is_higher": {"type": "boolean"},
        "unique_name": {"type": "string"},
    }
    if version == 'v2':
        p["node_id"] = {"type": "integer"}
        p["ot:ottId"] = {"type": "integer"}
    else:
        p["ott_id"] = {"type": "integer"}
    par["properties"] = p
    par["required"] = list(p.keys())
    par["required"].sort()


v2 = copy.deepcopy(current)
add_taxon_properties(current["items"], 'current')
add_taxon_properties(v2["items"], 'v2')
v3 = copy.deepcopy(current)
v2['$id'] = v2['$id'].replace('/current/', '/v3/')
v3['$id'] = v3['$id'].replace('/current/', '/v3/')

_version2schema = {'current': current, 'v2': v2, 'v3': v3}


def validate(doc, version='current'):
    jsonschema.validate(doc, _version2schema[version])
    return True
