#!/usr/bin/env python
# -*- coding: utf-8 -*-

from otwstest.schema.tree_of_life.induced_subtree import validate
from otwstest import all_api_versions, not_v2_version


@all_api_versions
def test_simple(outcome):
    url = outcome.make_url('tree_of_life/induced_subtree')
    ni = [3504, 396446]
    if outcome.api_version == 'v2':
        id_list = ni
    else:
        id_list = ['ott{}'.format(i) for i in ni]
    outcome.do_http_json(url, 'POST',
                         data={u'node_ids': id_list}, validator=validate)

@not_v2_version
def test_400_expected(outcome):
    url = outcome.make_url('tree_of_life/induced_subtree')
    data = {u"ott_ids": [292466, 501678, 267845, 666104, 316878, 102710, 176458]}
    outcome.do_http_json(url, 'POST',
                         data=data,
                         expected_status=400)
