#!/usr/bin/env python
from otwstest.schema.taxonomy.lica import validate

def test_bad_taxon(config, outcome):
    url = config.make_url('v2/taxonomy/lica')
    blob = outcome.do_http_json(url, 'POST', data={"ott_ids":[5551856,821970,770319]},
                                expected_status=200, validator=lambda x : validate(x, 'v2'))
    expected_id = 770319
    observered_id = blob['lica'][u'ot:ottId']
    if observered_id  != expected_id:
        m = 'Expected LICA ottId to be {} , found {}\n'.format(expected_id, observered_id)
        outcome.set_failure(m)
    if u'ott_ids_not_found' not in blob:
        m = "Expected to find list of ott_ids_not_found.\n"
        outcome.set_failure(m)
    bad_ids = blob[u'ott_ids_not_found']
    expected_bad_id = 5551856
    if expected_bad_id not in bad_ids:
        m = 'Expected to find {} in bad ids, found {}\n'.format(expected_bad_id, bad_ids)
        outcome.set_failure(m)

