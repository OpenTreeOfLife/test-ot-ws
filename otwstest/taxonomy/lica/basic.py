#!/usr/bin/env python
from otwstest.schema.taxonomy.lica import validate


def testsimple(config, outcome):
    url = config.make_url('v2/taxonomy/lica')
    outcome.do_http_json(url, 'POST', data={"ott_ids": [515698, 590452, 409712, 643717]},
                         expected_status=200, validator=lambda x: validate(x, 'v2'))


def testnoarg(config, outcome):
    url = config.make_url('v2/taxonomy/lica')
    outcome.do_http_json(url, 'POST', data={"ott_ids": []},
                         expected_status=200,
                         validator=lambda x: validate(x, 'v2'))
    outcome.store('improved_status', 400)


def test2(config, outcome):
    url = config.make_url('v2/taxonomy/lica')
    blob = outcome.do_http_json(url, 'POST', data={"ott_ids": [901642, 55033]},
                                expected_status=200, validator=lambda x: validate(x, 'v2'))
    expected_id = 637370
    observered_id = blob['lica'][u'ot:ottId']
    if observered_id != expected_id:
        m = 'Expected LICA ottId to be {} , found {}\n'.format(expected_id, observered_id)
        outcome.set_failure(m)
