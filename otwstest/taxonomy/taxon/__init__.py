#!/usr/bin/env python
# -*- coding: utf-8 -*-
from otwstest.schema.taxonomy.taxon import validate
from otwstest import demand_property


def test_simple(config, outcome):
    url = config.make_url('v2/taxonomy/taxon')
    result = outcome.do_http_json(url, 'POST', data={"ott_id": 901642},
                                  expected_status=200, validator=lambda x: validate(x, 'v2'))
    expected = u'Alseuosmia banksii'
    obs = result[u'ot:ottTaxonName']
    if obs != expected:
        errstr = 'Expected taxon name "{}", but found in "{}"'.format(expected, obs)
        outcome.exit_test_with_failure(errstr)


def _check_ott_id(result, outcome, ott_id, version):
    if version == 'v2':
        if result[u'ot:ottId'] != ott_id:
            errstr = 'Incorrect ott_id in returned taxon {}', format(result[u'ot:ottId'])
            outcome.exit_test_with_failure(errstr)


def test_include_children(config, outcome):
    url = config.make_url('v2/taxonomy/taxon')
    result = outcome.do_http_json(url, 'POST', data={"ott_id": 515698, "include_children": "true"},
                                  expected_status=200, validator=lambda x: validate(x, 'v2'))
    _check_ott_id(result, outcome, 515698, 'v2')
    demand_property(u'children', result, outcome, 'taxon')
    expected_child = 503056
    if expected_child not in map(lambda c: c[u'ot:ottId'], result[u'children']):
        errstr = 'Expected child {} not found in result'.format(expected_child)
        outcome.exit_test_with_failure(errstr)


def test_include_lineage(config, outcome):
    url = config.make_url('v2/taxonomy/taxon')
    result = outcome.do_http_json(url, 'POST', data={"ott_id": 515698, "include_lineage": "true"},
                                  expected_status=200, validator=lambda x: validate(x, 'v2'))
    _check_ott_id(result, outcome, 515698, 'v2')
    demand_property(u'taxonomic_lineage', result, outcome, 'taxon')
