#!/usr/bin/env python
# -*- coding: utf-8 -*-

from otwstest.schema.studies.find_trees import validate
from otwstest import is_str_type, all_api_versions


@all_api_versions
def test_find_by_ott_id(outcome):
    matched_studies = set()
    url = outcome.make_url('studies/find_trees')
    d = {'verbose': True,
         'property': 'ot:ottId',
         'value': '473875'}
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
            outcome.exit_test_with_failure(errstr.format(repr(type(sub))))
        for s in sub:
            matched_studies.add(s['ot:studyId'])
            if not isinstance(s, dict):
                errstr = 'expecting a list of dictionaries, found {}'
                outcome.exit_test_with_failure(errstr.format(repr(type(s))))
            errstr = 'Did not retrieve study: "{}"'.format(s.keys())
    if not "pg_704" in matched_studies:
        errstr = 'taxon ott473875 is in pg_704, but tree was not found.'
        outcome.exit_test_with_failure(errstr.format(repr(type(s))))
