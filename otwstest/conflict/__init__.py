#!/usr/bin/env python
# -*- coding: utf-8 -*-

# !/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from otwstest import is_str_type, all_api_versions
import otwstest.schema.tnrs as tnrs
from otwstest.schema.taxonomy.taxon import get_ott_id_property


@all_api_versions
def test_conflict_status_synth(outcome):  # Depends on study ot_1501 in phylesystem
    url = outcome.make_url('conflict/conflict-status')
    result = outcome.do_http_json(url, 'POST', data={'tree1': 'ot_1501#tree1',
                                                     'tree2': 'synth'})

@all_api_versions
def test_conflict_status_ott(outcome):  # Depends on study ot_1501 in phylesystem
    url = outcome.make_url('conflict/conflict-status')
    result = outcome.do_http_json(url, 'POST', data={'tree1': 'ot_1501#tree1',
                                                     'tree2': 'ott'})


# The website is using the GET versions, which are translated to POST in ws_wrapper.
@all_api_versions
def test_conflict_status_synth_get(outcome):  # Depends on study ot_1501 in phylesystem
    url = outcome.make_url('conflict/conflict-status?tree1=ot_1501%23tree1&tree2=synth')
    result = outcome.do_http_json(url, 'GET')

@all_api_versions
def test_conflict_status_ott_get(outcome):  # Depends on study ot_1501 in phylesystem
    url = outcome.make_url('conflict/conflict-status?tree1=ot_1501%23tree1&tree2=ott')
    result = outcome.do_http_json(url, 'GET')
