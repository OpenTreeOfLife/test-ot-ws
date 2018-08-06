#!/usr/bin/env python
# -*- coding: utf-8 -*-

from otwstest.schema.studies.find_studies import validate
from otwstest import all_api_versions


@all_api_versions
def test_find_by_doi(outcome):
    url = outcome.make_url('studies/find_studies')
    d = {'verbose': True,
         'property': 'ot:studyPublication',
         'value': '10.1600/036364408785679851', }
    outcome.do_http_json(url, verb='POST', data=d, validator=validate)
