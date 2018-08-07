#!/usr/bin/env python
# -*- coding: utf-8 -*-

from otwstest.schema.tree_of_life.node_info import validate
from otwstest import all_api_versions, not_v2_version


@all_api_versions
def test_simple(outcome):
    o = 396446
    if outcome.api_version == 'v2':
        url = outcome.make_url('graph/node_info')
        d = {'ott_id': o}
    else:
        url = outcome.make_url('tree_of_life/node_info')
        d = {'node_id': 'ott{}'.format(o)}
    outcome.do_http_json(url, 'POST', data=d, validator=validate)


@all_api_versions
def test_include_lineage(outcome):
    o = 396446
    if outcome.api_version == 'v2':
        url = outcome.make_url('graph/node_info')
        d = {'ott_id': o}
    else:
        url = outcome.make_url('tree_of_life/node_info')
        d = {'node_id': 'ott{}'.format(o)}
    d['include_lineage'] = True
    outcome.do_http_json(url, 'POST', data=d, validator=validate)


@not_v2_version
def test_mrca_designation(outcome):
    url = outcome.make_url('tree_of_life/node_info')
    d = {'node_id': 'mrcaott3504ott396446'}
    outcome.do_http_json(url, 'POST', data=d, validator=validate)
