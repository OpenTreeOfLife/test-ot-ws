#!/usr/bin/env python
from otwstest.schema.taxonomy.about import current, v2, v3

def tests(config, outcome):
    url = config.make_url('v2/taxonomy/about')
    outcome.do_http_json(url, 'POST', expected_status=200, schema=v2)
