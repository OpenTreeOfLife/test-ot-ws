#!/usr/bin/env python
# -*- coding: utf-8 -*-

from otwstest.schema.studies.properties import validate
from otwstest import all_api_versions


@all_api_versions
def test_properties(outcome):
    url = outcome.make_url('studies/properties')
    outcome.do_http_json(url, verb='POST', validator=validate)
