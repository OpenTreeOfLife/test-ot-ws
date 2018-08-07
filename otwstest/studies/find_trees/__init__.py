#!/usr/bin/env python
# -*- coding: utf-8 -*-

from otwstest.schema.studies.find_trees import validate
from otwstest import all_api_versions


@all_api_versions
def test_find_by_ott_id(outcome):
    url = outcome.make_url('studies/find_trees')
    d = {'verbose': True,
         'property': 'ot:ottId',
         'value': '770315'}
    outcome.do_http_json(url, verb='POST', data=d, validator=validate)

