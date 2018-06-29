#!/usr/bin/env python
# -*- coding: utf-8 -*-
from otwstest.schema.taxonomy.taxon import validate
import re


def test_simple(config, outcome):
    url = config.make_url('v2/taxonomy/taxon')
    result = outcome.do_http_json(url, 'POST', data={"ott_id": 901642},
                                  expected_status=200, validator=lambda x: validate(x, 'v2'))
    expected = u'Alseuosmia banksii'
    obs = result[u'ot:ottTaxonName']
    if obs != expected:
         errstr = 'Expected taxon name "{}", but found in "{}"'.format(expected, obs)
         outcome.exit_test_with_failure(errstr)

def test_include_children(config, outcome):
    url = config.make_url('v2/taxonomy/taxon')
    result = outcome.do_http_json(url, 'POST', data={"ott_id": 515698, "include_children": "true"},
                                  expected_status=200, validator=lambda x: validate(x, 'v2'))
    if result[u'ot:ottId'] != 515698:
        errstr = 'Incorrect ott_id in returned taxon {}', format(result[u'ot:ottId'])
        outcome.exit_test_with_failure(errstr)
    if u'children' not in result:
        errstr = 'No children returned when expected in taxon report.'
        outcome.exit_test_with_failure(errstr)
    expected_child = 503056
    if expected_child not in map(lambda c: c[u'ot:ottId'], result[u'children']):
        errstr = 'Expected child {} not found in result'.format(expected_child)
        outcome.exit_test_with_failure(errstr)


