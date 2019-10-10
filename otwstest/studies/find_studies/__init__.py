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

@all_api_versions
def test_find_by_curator(outcome):
    url = outcome.make_url('studies/find_studies')
    d = {'verbose': True,
         'property': 'ot:curatorName',
         'value': 'Emily Jane McTavish'}
    result = outcome.do_http_json(url, verb='POST', data=d, validator=validate)
    for top, sub in result.items():
        if not is_str_type(top):
            errstr = 'expecting keys of studies/properties to be strings found {}'
            outcome.exit_test_with_failure(errstr.format(repr(top)))
        if not top=="matched_studies":
            errstr = 'Top level key should be "matched_studies", actually is {}'
            outcome.exit_test_with_failure(errstr.format(repr(top)))
        if not isinstance(sub, list):
            errstr = 'expecting a list of matched studies, found {}'
            outcome.exit_test_with_failure(errstr.format(repr(sub)))
        for s in sub:
            if not is_str_type(s):
                errstr = 'expecting a list of strings found {}'
                outcome.exit_test_with_failure(errstr.format(repr(s)))
    for k in ('ot_209','ot_1059'):
        if k not in result:
            errstr = 'Did not retrieve study: "{}"'.format(k)
            outcome.exit_test_with_failure(errstr)
 #   if 'ot:studyPublication' not in result['study_properties']:
 #       errstr = 'ot:studyPublication not in study_properties'
 #       outcome.exit_test_with_failure(errstr)
 #   if 'ot:nodeLabelMode' not in result['tree_properties']:
 #       errstr = 'ot:nodeLabelMode not in tree_properties.'
 #       outcome.exit_test_with_failure(errstr)

