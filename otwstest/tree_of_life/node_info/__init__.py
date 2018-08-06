#!/usr/bin/env python
# -*- coding: utf-8 -*-

from otwstest.schema.tree_of_life.node_info import validate
from otwstest import all_api_versions, not_v2_version


@all_api_versions
def test_simple(outcome):
    if outcome.api_version == 'v2':
        url = outcome.make_url('graph/node_info')
        d = {'ott_id': 396446}
    else:
        url = outcome.make_url('tree_of_life/node_info')
        d = {'node_id': 'mrcaott3504ott396446'}
    outcome.do_http_json(url, 'POST', data=d, validator=validate)


