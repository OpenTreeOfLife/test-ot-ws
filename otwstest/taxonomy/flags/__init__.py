#!/usr/bin/env python
# -*- coding: utf-8 -*-

from otwstest.schema.taxonomy.flags import validate
from otwstest import all_api_versions


@all_api_versions
def test_simple(outcome):
    url = outcome.make_url('taxonomy/flags')
    outcome.do_http_json(url, 'POST', validator=validate)
