#!/usr/bin/env python
from otwstest.schema.taxonomy.about import validate

def tests(config, outcome):
    url = config.make_url('v2/taxonomy/lica')
    outcome.do_http_json(url, 'POST', data={"ott_ids":[515698,590452,409712,643717]},
                         expected_status=200, validator=lambda x : validate(x, 'v2'))
