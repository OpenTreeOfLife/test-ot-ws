#!/usr/bin/env python
# -*- coding: utf-8 -*-

from otwstest.schema.studies.find_studies import validate
from otwstest import all_api_versions


@all_api_versions
def test_find_by_doi(outcome):
    url = outcome.make_url('studies/find_studies')
    d = {'verbose': True,
         'property': 'ot:studyPublication',
         'value': 'http://dx.doi.org/10.1073/pnas.0308657101', }
    outcome.do_http_json(url, verb='POST', data=d, validator=validate)


@all_api_versions
def test_find_all(outcome):
    url = outcome.make_url('studies/find_studies')
    outcome.do_http_json(url, verb='POST', validator=validate)
