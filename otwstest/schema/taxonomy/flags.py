#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import jsonschema

current = {
    "$id": "https://tree.opentreeoflife.org/schema/current/taxonomy/flags.json",
    "type": "object",
    "$schema": "http://json-schema.org/draft-07/schema#",
    "properties": {
        "barren": {"type": "integer"},
        "edited": {"type": "integer"},
        "environmental": {"type": "integer"},
        "environmental_inherited": {"type": "integer"},
        "extinct": {"type": "integer"},
        "extinct_direct": {"type": "integer"},
        "extinct_inherited": {"type": "integer"},
        "forced_visible": {"type": "integer"},
        "hidden": {"type": "integer"},
        "hidden_inherited": {"type": "integer"},
        "hybrid": {"type": "integer"},
        "incertae_sedis": {"type": "integer"},
        "incertae_sedis_direct": {"type": "integer"},
        "incertae_sedis_inherited": {"type": "integer"},
        "inconsistent": {"type": "integer"},
        "infraspecific": {"type": "integer"},
        "major_rank_conflict": {"type": "integer"},
        "major_rank_conflict_direct": {"type": "integer"},
        "major_rank_conflict_inherited": {"type": "integer"},
        "merged": {"type": "integer"},
        "not_otu": {"type": "integer"},
        "sibling_higher": {"type": "integer"},
        "sibling_lower": {"type": "integer"},
        "tattered": {"type": "integer"},
        "tattered_inherited": {"type": "integer"},
        "unclassified": {"type": "integer"},
        "unclassified_direct": {"type": "integer"},
        "unclassified_inherited": {"type": "integer"},
        "unplaced": {"type": "integer"},
        "unplaced_inherited": {"type": "integer"},
        "viral": {"type": "integer"},
        "was_container": {"type": "integer"}
    },
    "required": ['barren', 'edited', 'environmental', 'environmental_inherited', 'extinct',
                 'extinct_direct', 'extinct_inherited', 'forced_visible', 'hidden',
                 'hidden_inherited', 'hybrid', 'incertae_sedis', 'incertae_sedis_direct',
                 'incertae_sedis_inherited', 'inconsistent', 'infraspecific', 'major_rank_conflict',
                 'major_rank_conflict_direct', 'major_rank_conflict_inherited', 'merged', 'not_otu',
                 'sibling_higher', 'sibling_lower', 'tattered', 'tattered_inherited',
                 'unclassified',
                 'unclassified_direct', 'unclassified_inherited', 'unplaced', 'unplaced_inherited',
                 'viral', 'was_container']
}

v3 = copy.deepcopy(current)
v3['$id'] = v3['$id'].replace('/current/', '/v3/')
v2 = copy.deepcopy(current)
v2['$id'] = v2['$id'].replace('/current/', '/v3/')

_version2schema = {'current': current, 'v2': v2, 'v3': v3}


def validate(doc, version='current'):
    schema = _version2schema[version]
    jsonschema.validate(doc, schema)
    for p in schema["required"]:
        if doc[p] < 0:
            m = 'Expecting "{}" field to be non-negative, found "{}"'.format(p, doc[p])
            raise jsonschema.ValidationError(m)
    return True
