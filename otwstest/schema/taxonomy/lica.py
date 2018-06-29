#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import jsonschema
from .taxon import taxon_obj_properties
current = {
    "$id": "https://tree.opentreeoflife.org/schema/current/taxonomy/lica.json",
    "type": "object",
    "definitions": {},
    "$schema": "http://json-schema.org/draft-07/schema#",
    "properties": {
        "lica": {
            "type": "object"
        },
        "ott_ids_not_found": {
            "type": "array",
            "items": {"type": "integer"}
        }
    }
}

v2 = copy.deepcopy(current)
v2['properties']['lica']['properties'] = taxon_obj_properties('v2')
current['properties']['lica']['properties'] = taxon_obj_properties('v3')
v3 = copy.deepcopy(current)
v3['$id'] = v3['$id'].replace('/current/', '/v3/')
v2['$id'] = v2['$id'].replace('/current/', '/v3/')

_version2schema = {'current': current, 'v2': v2, 'v3': v3}


def validate(doc, version='current'):
    schema = _version2schema[version]
    jsonschema.validate(doc, schema)
    return True
