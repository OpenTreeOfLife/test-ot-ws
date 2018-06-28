#!/usr/bin/env python
from otwstest.schema.taxonomy.lica import validate

def testsimple(config, outcome):
    url = config.make_url('v2/taxonomy/lica')
    outcome.do_http_json(url, 'POST', data={"ott_ids":[515698,590452,409712,643717]},
                         expected_status=200, validator=lambda x : validate(x, 'v2'))

def testnoarg(config, outcome):
    url = config.make_url('v2/taxonomy/lica')
    outcome.do_http_json(url, 'POST', data={"ott_ids": []},
                         expected_status=200,
                         validator=lambda x: validate(x, 'v2'))
    outcome.store('improved_status', 400)

