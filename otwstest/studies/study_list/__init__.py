#!/usr/bin/env python
# -*- coding: utf-8 -*-

from otwstest import all_api_versions
import jsonschema
from otwstest.schema.primitives import SCHEMA_ARRAY_OF_STRINGS

def validate(doc, version='current'):
    schema = SCHEMA_ARRAY_OF_STRINGS()
    jsonschema.validate(doc, schema)
    return True

@all_api_versions
def test_get_tree_nexus(outcome):
    url = outcome.make_url('study_list')
    outcome.do_http_json(url, validator=validate)
