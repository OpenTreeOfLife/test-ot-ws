#!/usr/bin/env python
# -*- coding: utf-8 -*-

# !/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from otwstest import is_str_type
import otwstest.schema.tnrs as tnrs


def test_autocomplete_name(config, outcome):  # taxonomy-sensitive test
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


def test_contexts(config, outcome):  # taxonomy-sensitive test
    url = config.make_url('v2/tnrs/contexts')
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
    for k in ('PLANTS', 'ANIMALS', 'FUNGI', 'LIFE', 'MICROBES'):
        if k not in result:
            errstr = 'Missing key in context listing: "{}"'.format(k)
            outcome.exit_test_with_failure(errstr)
    if 'Archaea' not in result['MICROBES']:
        errstr = 'Archaea not in context MICROBES'
        outcome.exit_test_with_failure(errstr)
    if 'Arachnids' not in result['ANIMALS']:
        errstr = 'Arachnides not in context ANIMALS.'
        outcome.exit_test_with_failure(errstr)


def test_infer_context(config, outcome):  # taxonomy-sensitive test
    url = config.make_url('v2/tnrs/infer_context')
    data = {"names": ["Pan", "Homo", "Mus musculus", "Upupa epops"]}
    result = outcome.do_http_json(url, 'POST', data=data,
                                  validator=lambda x: tnrs.infer_context.validate(x, 'v2'))
    if result['context_name'] != 'Tetrapods':
        errstr = 'Expected context_name = Tetrapods, found "{}"'.format(result['context_name'])
        outcome.exit_test_with_failure(errstr)
    if result['ambiguous_names']:
        errstr = 'Expected no ambiguous_names, but found {}.'.format(result['ambiguous_names'])
        outcome.exit_test_with_failure(errstr)


def test_match_names(config, outcome):  # taxonomy-sensitive test
    url = config.make_url('v2/tnrs/match_names')
    test_list = ["Aster", "Symphyotrichum", "Erigeron", "Barnadesia", "Hylobates"]
    test_ids = [409712, 1058735, 643717, 515698, 166552]
    data = {"names": test_list}
    result = outcome.do_http_json(url, 'POST', data=data,
                                  validator=lambda x: tnrs.match_names.validate(x, 'v2'))
    mni = result[u'matched_name_ids']
    if set(test_list) != set(mni):
        errstr = "Failed to match, submitted: {}, returned {}"
        outcome.exit_test_with_failure(errstr.format(test_list, mni))
    match_list = result['results']
    for match in match_list:
        m = match['matches'][0]
        if m.get(u'ot:ottId') not in test_ids:
            errstr = "bad match return {}, expected one of {}"
            outcome.exit_test_with_failure(errstr.format(m.get(u'ot:ottId'), test_ids))
        if m.get(u'matched_name') not in test_list:
            errstr = "bad match return {}, expected one of {}"
            outcome.exit_test_with_failure(errstr.format(m.get(u'matched_name'), test_list))
'''
TEST_LIST = ["Hylobates"]
TEST_IDS = [166552]
test, result = test_http_json_method(SUBMIT_URI, "POST",
                                        data={"names":TEST_LIST, "context_name": 'Mammals'},
                                        expected_status=200,
                                        return_bool_data=True)
if not test:
    sys.exit(1)
if set(TEST_LIST) != set(result[u'matched_name_ids']):
    errstr = "Failed to match, submitted: {}, returned {}\n"
    sys.stderr.write(errstr.format(TEST_LIST,result[u'matched_name_ids']))
    sys.exit(1)
MATCH_LIST = result['results']
for match in MATCH_LIST:
    m = match[u'matches'][0]
    if m[u'matched_name'] not in TEST_LIST:
        errstr = "bad match return {}, expected one of {}\n"
        sys.stderr.write(errstr.format(m[u'matched_name'],str(TEST_LIST)))
        sys.exit(1)
    if m[u'ot:ottId'] not in TEST_IDS:
        errstr = "bad match return {}, expected one of {}\n"
        sys.stderr.write(errstr.format(m[u'ot:ottId'],str(TEST_IDS)))
        sys.exit(1)
'''