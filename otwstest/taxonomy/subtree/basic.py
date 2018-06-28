#!/usr/bin/env python
from otwstest.schema.taxonomy.subtree import validate
import re
def testsimple(config, outcome):
    url = config.make_url('v2/taxonomy/subtree')
    result = outcome.do_http_json(url, 'POST', data={"ott_id":515698},
                                  expected_status=200, validator=lambda x : validate(x, 'v2'))
    tree = result[u'subtree']
    ROOTTAXONSTR = r"\)Barnadesia_ott515698;"
    namecheck =  re.compile(ROOTTAXONSTR)
    if re.search(namecheck, tree) is None:
        errstr = 'substring {} does not appear at root of tree:\n {}'
        errstr = errstr.format(ROOTTAXONSTR, tree)
        outcome.set_failure(errstr)