#!/usr/bin/env python
# -*- coding: utf-8 -*-

from otwstest import all_api_versions


@all_api_versions
def test_file(outcome):
    study_id = 'ot_134'
    url = outcome.make_url('study/{}/file'.format(study_id))
    x = outcome.do_http_json(url)
    if len(x) == 0:
        m = 'expecting study {} to have an attached file.'.format(study_id)
        outcome.exit_test_with_failure(m)
    file_id = x[0]['id']
    url = outcome.make_url('study/{}/file/{}'.format(study_id, file_id))
    outcome.do_http_json(url, return_raw_content=True)

