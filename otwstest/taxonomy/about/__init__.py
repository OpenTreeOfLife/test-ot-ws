#!/usr/bin/env python
# -*- coding: utf-8 -*-

from otwstest.schema.taxonomy.about import validate


def test_simple(config, outcome):
    url = config.make_url('v2/taxonomy/about')
    outcome.do_http_json(url, 'POST', validator=lambda x: validate(x, 'v2'))
