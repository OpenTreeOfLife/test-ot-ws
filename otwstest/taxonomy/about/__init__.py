#!/usr/bin/env python
# -*- coding: utf-8 -*-

from otwstest.schema.taxonomy.about import validate
from otwstest import all_api_versions


@all_api_versions
def test_simple(outcome):
    url = outcome.make_url('taxonomy/about')
    outcome.do_http_json(url, 'POST', validator=validate)
