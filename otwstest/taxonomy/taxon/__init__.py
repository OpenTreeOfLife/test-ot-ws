#!/usr/bin/env python
# -*- coding: utf-8 -*-
from otwstest.schema.taxonomy.subtree import validate
import re


def test_simple(config, outcome):
    url = config.make_url('v2/taxonomy/taxon')
    result = outcome.do_http_json(url, 'POST', data={"ott_id": 901642},
                                  expected_status=200, validator=lambda x: validate(x, 'v2'))
    # TEST_NAME = u'Alseuosmia banksii'
    # if u'ot:ottTaxonName' not in result:
    #     sys.stderr.write('ot:ottTaxonName not returned in result\n')
    #     sys.exit(1)
    # taxonName = result[u'ot:ottTaxonName']
    # if taxonName != TEST_NAME:
    #     errstr = 'Expected taxon name {} but not found in \n{}\n'
    #     sys.stderr.write(errstr.format(TEST_NAME,taxonName))
    #     sys.exit(1)


