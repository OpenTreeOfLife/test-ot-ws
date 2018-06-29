#!/usr/bin/env python
# -*- coding: utf-8 -*-

from otwstest.schema.taxonomy.flags import validate


def test_simple(config, outcome):
    url = config.make_url('v2/taxonomy/flags')
    outcome.do_http_json(url, 'POST', expected_status=200, validator=lambda x: validate(x, 'v2'))
