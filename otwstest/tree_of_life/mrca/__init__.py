#!/usr/bin/env python
# -*- coding: utf-8 -*-

from otwstest.schema.tree_of_life.mrca import validate
from otwstest import all_api_versions, not_v2_version


@all_api_versions
def test_simple(outcome):
    url = outcome.make_url('tree_of_life/mrca')
    id_list = [1084532, 3826]
    outcome.do_http_json(url, 'POST', data={u'ott_ids': id_list}, validator=validate)


@not_v2_version
def test_400(outcome):
    url = outcome.make_url('tree_of_life/mrca')
    id_list = [1084532, 3826, 2, 3, 5]
    outcome.do_http_json(url, 'POST', data={u'ott_ids': id_list}, expected_status=400)

