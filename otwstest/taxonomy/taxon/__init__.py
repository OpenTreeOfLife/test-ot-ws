#!/usr/bin/env python
# -*- coding: utf-8 -*-
from otwstest.schema.taxonomy.taxon import validate
from otwstest import demand_property


def test_simple(outcome):  # taxonomy-sensitive test
    url = outcome.make_url('taxonomy/taxon')
    result = outcome.do_http_json(url, 'POST', data={"ott_id": 901642}, validator=validate)
    expected = u'Alseuosmia banksii'
    obs = result[u'ot:ottTaxonName']
    if obs != expected:
        errstr = 'Expected taxon name "{}", but found in "{}"'.format(expected, obs)
        outcome.exit_test_with_failure(errstr)


test_simple.api_versions = ('v2', 'v3')


def _check_ott_id(result, outcome, ott_id):
    if outcome.api_version == 'v2':
        if result[u'ot:ottId'] != ott_id:
            errstr = 'Incorrect ott_id in returned taxon {}', format(result[u'ot:ottId'])
            outcome.exit_test_with_failure(errstr)
    else:
        NotImplementedError('v3')


def test_include_children(outcome):  # taxonomy-sensitive test
    url = outcome.make_url('taxonomy/taxon')
    result = outcome.do_http_json(url, 'POST', data={"ott_id": 515698, "include_children": "true"},
                                  validator=validate)
    _check_ott_id(result, outcome, 515698, )
    demand_property(u'children', result, outcome, 'taxon')
    expected_child = 503056
    if expected_child not in map(lambda c: c[u'ot:ottId'], result[u'children']):
        errstr = 'Expected child {} not found in result'.format(expected_child)
        outcome.exit_test_with_failure(errstr)


test_include_children.api_versions = ('v2', 'v3')


def test_include_lineage(outcome):
    url = outcome.make_url('taxonomy/taxon')
    result = outcome.do_http_json(url, 'POST', data={"ott_id": 515698, "include_lineage": "true"},
                                  validator=validate)
    _check_ott_id(result, outcome, 515698)
    demand_property('taxonomic_lineage', result, outcome, 'taxon')


test_include_lineage.api_versions = ('v2', 'v3')


def test_tax_sources(outcome):  # taxonomy-sensitive test
    url = outcome.make_url('taxonomy/taxon')
    result = outcome.do_http_json(url, 'POST', data={"ott_id": 766177}, validator=validate)
    sources = demand_property('tax_sources', result, outcome, 'taxon')
    for e in ['ncbi:58228', 'gbif:3189571', 'irmng:11346207']:
        if e not in sources:
            errstr = 'Expected "{}" not found in tax_sources'.format(e)
            outcome.exit_test_with_failure(errstr)


test_tax_sources.api_versions = ('v2', 'v3')


def test_terminal(outcome):  # taxonomy-sensitive test
    url = outcome.make_url('taxonomy/taxon')
    result = outcome.do_http_json(url, 'POST', data={"ott_id": 1066581,
                                                     "list_terminal_descendants": True},
                                  validator=validate)
    descendants = demand_property('terminal_descendants', result, outcome, 'taxon')
    if not {490099, 1066590}.issubset(set(descendants)):
        errstr = "Bos taurus (490099) and Bos primigenius (1066590) not returned as " \
                 "descendants of Bos (1066581)\n"
        outcome.exit_test_with_failure(errstr)


test_terminal.api_versions = ('v2', 'v3')
