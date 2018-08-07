#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import jsonschema
from otwstest import compose_schema2version, SCHEMA_URL_PREF
from otwstest.schema.primitives import (SCHEMA_INTEGER,
                                        SCHEMA_STRING, SCHEMA_ARRAY_OBJECTS,)

def get_find_studies_properties(version):
    p = ["ot:studyPublicationReference", "ot:curatorName",
         "ot:studyId", "ot:studyYear", "ot:focalClade",
         "ot:focalCladeOTTTaxonName", "ot:dataDeposit", "ot:studyPublication"
        ]
    pd = {}
    for prop in p:
        pd[prop] = SCHEMA_STRING()
    for prop in ["ot:studyYear",  "ot:focalClade"]:
        pd[prop] = SCHEMA_INTEGER()
    ms = SCHEMA_ARRAY_OBJECTS()
    ms['items']['properties'] = pd
    return {'matched_studies': ms}

_version2schema = None


def get_version2schema():
    global _version2schema
    if _version2schema is not None:
        return _version2schema
    current = {
        "$id": SCHEMA_URL_PREF + "current/tree_of_life/about.json",
        "type": "object",
        "$schema": "http://json-schema.org/draft-07/schema#",
        "properties": get_find_studies_properties('v3'),
        "required": ["matched_studies"]
    }
    v2 = copy.deepcopy(current)
    p2 = get_find_studies_properties('v2')
    v2["properties"] = p2
    v2["required"] = list(p2.keys())
    _version2schema = compose_schema2version(v2=v2, current=current)
    return get_version2schema()


def schema_for_version(version):
    return get_version2schema()[version]


def validate(doc, version='current'):
    jsonschema.validate(doc, schema_for_version(version))
    return True
