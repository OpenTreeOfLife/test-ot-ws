#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import jsonschema

current = {
    "$id": "https://tree.opentreeoflife.org/schema/current/tnrs/infer_context.json",
    "type": "object",
    "$schema": "http://json-schema.org/draft-07/schema#",
    "properties": {
        "ambiguous_names": {"type": "array",
                            "items": {"type": "string"}
                           },
        "context_name": {"type": "string"},
        "context_ott_id": {"type": "integer"}
    },
    "required": ["ambiguous_names", "context_name", "context_ott_id"]
}

v2 = copy.deepcopy(current)
v3 = copy.deepcopy(current)
v2['$id'] = v2['$id'].replace('/current/', '/v3/')
v3['$id'] = v3['$id'].replace('/current/', '/v3/')

_version2schema = {'current': current, 'v2': v2, 'v3': v3}


def validate(doc, version='current'):
    jsonschema.validate(doc, _version2schema[version])
    return True
