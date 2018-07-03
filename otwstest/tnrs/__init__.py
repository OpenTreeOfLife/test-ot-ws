#!/usr/bin/env python
# -*- coding: utf-8 -*-

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from otwstest.schema.tnrs.autocomplete_name import validate

def test_autocomplete_name(config, outcome):  #taxonomy-sensitive test
    url = config.make_url('v2/tnrs/autocomplete_name')
    search_name = "Endoxyla"
    result = outcome.do_http_json(url, 'POST', data={"name": search_name,
                                                     "context_name": "All life"},
                                  expected_status=200, validator=lambda x: validate(x, 'v2'))
    for res in result:
        uname = res["unique_name"]
        if not re.search(search_name, uname):
            errstr = 'unique_name: "{}" of taxon record does not contain search string "{}"'
            outcome.exit_test_with_failure(errstr.format(uname, search_name))


