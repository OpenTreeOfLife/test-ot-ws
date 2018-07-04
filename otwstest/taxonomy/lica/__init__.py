#!/usr/bin/env python
# -*- coding: utf-8 -*-

from otwstest.schema.taxonomy.lica import validate


def test_bad_taxon(config, outcome):
    url = config.make_url('v2/taxonomy/lica')
    expected_bad_id = 55518566
    blob = outcome.do_http_json(url, 'POST', data={"ott_ids": [expected_bad_id, 821970, 770319]},
                                validator=lambda x: validate(x, 'v2'))
    expected_id = 770319
    observered_id = blob['lica'][u'ot:ottId']
    if observered_id != expected_id:
        m = 'Expected LICA ottId to be {} , found {}\n'.format(expected_id, observered_id)
        outcome.exit_test_with_failure(m)
    if u'ott_ids_not_found' not in blob:
        m = "Expected to find list of ott_ids_not_found.\n"
        outcome.exit_test_with_failure(m)
    bad_ids = blob[u'ott_ids_not_found']
    if expected_bad_id not in bad_ids:
        m = 'Expected to find {} in bad ids, found {}\n'.format(expected_bad_id, bad_ids)
        outcome.exit_test_with_failure(m)


def test_simple(config, outcome):
    url = config.make_url('v2/taxonomy/lica')
    outcome.do_http_json(url, 'POST', data={"ott_ids": [515698, 590452, 409712, 643717]},
                         validator=lambda x: validate(x, 'v2'))


def test_no_arg(config, outcome):
    url = config.make_url('v2/taxonomy/lica')
    outcome.do_http_json(url, 'POST', data={"ott_ids": []},
                         validator=lambda x: validate(x, 'v2'))
    outcome.store('improved_status', 400)


def test_2(config, outcome):
    url = config.make_url('v2/taxonomy/lica')
    blob = outcome.do_http_json(url, 'POST', data={"ott_ids": [901642, 55033]},
                                validator=lambda x: validate(x, 'v2'))
    expected_id = 637370
    observered_id = blob['lica'][u'ot:ottId']
    if observered_id != expected_id:
        m = 'Expected LICA ottId to be {} , found {}\n'.format(expected_id, observered_id)
        outcome.exit_test_with_failure(m)
