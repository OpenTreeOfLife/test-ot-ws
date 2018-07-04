#!/usr/bin/env python
# -*- coding: utf-8 -*-
from otwstest.schema.taxonomy.taxon import validate
from otwstest import demand_property


def test_simple(config, outcome):  #taxonomy-sensitive test
    url = config.make_url('v2/taxonomy/taxon')
    result = outcome.do_http_json(url, 'POST', data={"ott_id": 901642},
                                  validator=lambda x: validate(x, 'v2'))
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


def test_include_children(config, outcome):  #taxonomy-sensitive test
    url = config.make_url('v2/taxonomy/taxon')
    result = outcome.do_http_json(url, 'POST', data={"ott_id": 515698, "include_children": "true"},
                                  validator=lambda x: validate(x, 'v2'))
    _check_ott_id(result, outcome, 515698, 'v2')
    demand_property(u'children', result, outcome, 'taxon')
    expected_child = 503056
    if expected_child not in map(lambda c: c[u'ot:ottId'], result[u'children']):
        errstr = 'Expected child {} not found in result'.format(expected_child)
        outcome.exit_test_with_failure(errstr)


def test_include_lineage(config, outcome):
    url = config.make_url('v2/taxonomy/taxon')
    result = outcome.do_http_json(url, 'POST', data={"ott_id": 515698, "include_lineage": "true"},
                                  validator=lambda x: validate(x, 'v2'))
    _check_ott_id(result, outcome, 515698, 'v2')
    demand_property('taxonomic_lineage', result, outcome, 'taxon')


def test_tax_sources(config, outcome):  #taxonomy-sensitive test
    url = config.make_url('v2/taxonomy/taxon')
    result = outcome.do_http_json(url, 'POST', data={"ott_id": 766177},
                                  validator=lambda x: validate(x, 'v2'))
    sources = demand_property('tax_sources', result, outcome, 'taxon')
    for e in ['ncbi:58228', 'gbif:3189571', 'irmng:11346207']:
        if e not in sources:
            errstr = 'Expected "{}" not found in tax_sources'.format(e)
            outcome.exit_test_with_failure(errstr)

def test_tax_sources(config, outcome):  #taxonomy-sensitive test
    url = config.make_url('v2/taxonomy/taxon')
    result = outcome.do_http_json(url, 'POST', data={"ott_id": 1066581,
                                                     "list_terminal_descendants": True},
                                  validator=lambda x: validate(x, 'v2'))
    descendants = demand_property('terminal_descendants', result, outcome, 'taxon')
    if not set([490099, 1066590]).issubset(set(descendants)):
        errstr = "Bos taurus (490099) and Bos primigenius (1066590) not returned as " \
                "descendants of Bos (1066581)\n"
        outcome.exit_test_with_failure(errstr)

