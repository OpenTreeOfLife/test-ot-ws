#!/usr/bin/env python
# -*- coding: utf-8 -*-
from otwstest.schema.taxonomy.taxon import validate
import re


def test_simple(config, outcome):
    url = config.make_url('v2/taxonomy/taxon')
    result = outcome.do_http_json(url, 'POST', data={"ott_id": 901642},
                                  expected_status=200, validator=lambda x: validate(x, 'v2'))
    expected = u'Alseuosmia banksii'
    obs = result[u'ot:ottTaxonName']
    if obs != expected:
         errstr = 'Expected taxon name "{}", but found in "{}"'.format(expected, obs)
         outcome.exit_test_with_failure(errstr)


