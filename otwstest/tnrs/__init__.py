#!/usr/bin/env python
# -*- coding: utf-8 -*-

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from otwstest import is_str_type
import otwstest.schema.tnrs as tnrs

def test_autocomplete_name(config, outcome):  #taxonomy-sensitive test
    url = config.make_url('v2/tnrs/autocomplete_name')
    search_name = "Endoxyla"
    result = outcome.do_http_json(url, 'POST', data={"name": search_name,
                                                     "context_name": "All life"},
                                  validator=lambda x: tnrs.autocomplete_name.validate(x, 'v2'))
    for res in result:
        uname = res["unique_name"]
        if not re.search(search_name, uname):
            errstr = 'unique_name: "{}" of taxon record does not contain search string "{}"'
            outcome.exit_test_with_failure(errstr.format(uname, search_name))


def test_contexts(config, outcome):  #taxonomy-sensitive test
    url = config.make_url('v2/tnrs/contexts')
    search_name = "Endoxyla"
    result = outcome.do_http_json(url, 'POST')
    for top, sub in result.items():
        if not is_str_type(top):
            errstr = 'expecting keys of tnrs/contexts to be strings found {}'
            outcome.exit_test_with_failure(errstr.format(repr(top)))
        if not isinstance(sub, list):
            errstr = 'expecting values of tnrs/contexts to be a list of strings found {}'
            outcome.exit_test_with_failure(errstr.format(repr(sub)))
        for s in sub:
            if not is_str_type(s):
                errstr = 'expecting values of tnrs/contexts to be a list of strings found {}'
                outcome.exit_test_with_failure(errstr.format(repr(s)))




