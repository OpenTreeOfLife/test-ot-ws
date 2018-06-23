#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import jsonschema

current = {
  "$id": "https://tree.opentreeoflife.org/schema/current/taxonomy/about.json",
  "type": "object",
  "$schema": "http://json-schema.org/draft-07/schema#",
  "properties": {
    "author": {
      "$id": "/properties/author",
      "type": "string",
      "default": "",
      "examples": [
        "open tree of life project"
      ]
    },
    "name": {
      "$id": "/properties/name",
      "type": "string",
      "default": "",
      "examples": [
        "ott"
      ]
    },
    "source": {
      "$id": "/properties/source",
      "type": "string",
      "default": "",
      "examples": [
        "ott3.0draft6"
      ]
    },
    "version": {
      "$id": "/properties/version",
      "type": "string",
      "default": "",
      "examples": [
        "3.0"
      ]
    },
    "weburl": {
      "$id": "/properties/weburl",
      "type": "string",
      "default": "",
      "examples": [
        "https://tree.opentreeoflife.org/about/taxonomy-version/ott3.0"
      ]
    }
  },
  "required": ["author", "name", "source", "version", "weburl"]
}

v3 = copy.deepcopy(current)
v3['$id'] = v3['$id'].replace('/current/', '/v3/')
v2 = copy.deepcopy(current)
v2['$id'] = v2['$id'].replace('/current/', '/v3/')

_version2schema = {'current': current, 'v2': v2, 'v3': v3}

def validate(doc, version='current'):
    jsonschema.validate(doc, _version2schema[version])
    if not doc["weburl"].startswith('http'):
        m = 'Expecting "weburl" field to start with http found "{}"'.format(doc['weburl'])
        raise jsonschema.ValidationError(m)
    return True

