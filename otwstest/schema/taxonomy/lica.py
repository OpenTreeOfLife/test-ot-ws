#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import jsonschema

current = {
  "$id": "https://tree.opentreeoflife.org/schema/current/taxonomy/flags.json",
  "type": "object",
  "definitions": {},
  "$schema": "http://json-schema.org/draft-07/schema#",
  "properties": {
    "lica": {
      "type": "object",
      "properties": {
        "flags": {
          "type": "array",
          "items": {"type": "string"}
        },
        "node_id": {"type": "integer"},
        "ot:ottId": {"type": "integer"},
        "ot:ottTaxonName": {"type": "string"},
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
    },
    "ott_ids_not_found": {
      "type": "array",
      "items": {"type": "integer"}
    }
  }
}

v3 = copy.deepcopy(current)
v3['$id'] = v3['$id'].replace('/current/', '/v3/')
v2 = copy.deepcopy(current)
v2['$id'] = v2['$id'].replace('/current/', '/v3/')

_version2schema = {'current': current, 'v2': v2, 'v3': v3}

def validate(doc, version='current'):
    schema = _version2schema[version]
    jsonschema.validate(doc, schema)
    return True

