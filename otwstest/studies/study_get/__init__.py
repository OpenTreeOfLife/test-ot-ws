#!/usr/bin/env python
# -*- coding: utf-8 -*-

from otwstest import all_api_versions
import jsonschema
from otwstest.schema.primitives import SCHEMA_ARRAY_OF_STRINGS


# noinspection PyUnusedLocal
def validate(doc, version='current'):
    schema = SCHEMA_ARRAY_OF_STRINGS()
    jsonschema.validate(doc, schema)
    return True


@all_api_versions
def test_404(outcome):
    url = outcome.make_url('study/1')
    outcome.do_http_json(url, expected_status=404)


@all_api_versions
def test_get(outcome):
    url = outcome.make_url('study/pg_10')
    n2jv = '1.2'
    x = outcome.do_http_json(url, data={'output_nexml2json': n2jv})
    try:
        if n2jv not in x['data']['nexml']["@nexml2json"]:
            m = 'did not get requested version ({}) of nexml2json'.format(n2jv)
            outcome.exit_test_with_failure(m)
    except Exception:
        outcome.exit_test_with_failure('response was not in nexml2json form')


@all_api_versions
def test_get_oldversion_nexml2json(outcome):
    url = outcome.make_url('study/pg_10')
    n2jv = '1.0'
    x = outcome.do_http_json(url, data={'output_nexml2json': n2jv})
    try:
        if n2jv not in x['data']['nexml']["@nexml2json"]:
            m = 'did not get requested version ({}) of nexml2json'.format(n2jv)
            outcome.exit_test_with_failure(m)
    except Exception:
        outcome.exit_test_with_failure('response was not in nexml2json form')
