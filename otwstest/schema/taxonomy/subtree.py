#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import jsonschema

current = {
    "$id": "https://tree.opentreeoflife.org/schema/current/taxonomy/subtree.json",
    "type": "object",
    "$schema": "http://json-schema.org/draft-07/schema#",
    "properties": {
        "subtree": {"type": "string"}
    },
    "required": ["subtree"]
}

v3 = copy.deepcopy(current)
v3['$id'] = v3['$id'].replace('/current/', '/v3/')
v2 = copy.deepcopy(current)
v2['$id'] = v2['$id'].replace('/current/', '/v3/')

_version2schema = {'current': current, 'v2': v2, 'v3': v3}


def validate(doc, version='current'):
    schema = _version2schema[version]
    jsonschema.validate(doc, schema)
    s = doc["subtree"]
    if not s.startswith('('):
        c = s if len(s) == 0 else s[0]
        m = 'Expecting "subtree" field to be start with a ( found "{}"'.format(c)
        raise jsonschema.ValidationError(m)
    return True
