#!/usr/bin/env python
# -*- coding: utf-8 -*-

from otwstest.schema.studies.properties import validate
from otwstest import is_str_type, all_api_versions



@all_api_versions
def test_properties(outcome):
    url = outcome.make_url('studies/properties')
    result = outcome.do_http_json(url, verb='POST', validator=validate)
    for top, sub in result.items():
        if not is_str_type(top):
            errstr = 'expecting keys of studies/properties to be strings found {}'
            outcome.exit_test_with_failure(errstr.format(repr(top)))
        if not isinstance(sub, list):
            errstr = 'expecting keys of studies/properties to be a list of strings found {}'
            outcome.exit_test_with_failure(errstr.format(repr(sub)))
        for s in sub:
            if not is_str_type(s):
                errstr = 'expecting keys of studies/properties to be a list of strings found {}'
                outcome.exit_test_with_failure(errstr.format(repr(s)))
    for k in ('tree_properties', 'study_properties'):
        if k not in result:
            errstr = 'Missing key in context listing: "{}"'.format(k)
            outcome.exit_test_with_failure(errstr)
    if 'ot:studyPublication' not in result['study_properties']:
        errstr = 'ot:studyPublication not in study_properties'
        outcome.exit_test_with_failure(errstr)
    if 'ot:nodeLabelMode' not in result['tree_properties']:
        errstr = 'ot:nodeLabelMode not in tree_properties.'
        outcome.exit_test_with_failure(errstr)
    if 'ot:ottId' not in result['tree_properties']:
        errstr = 'ot:nodeLabelMode not in tree_properties.'
        outcome.exit_test_with_failure(errstr)