#!/usr/bin/env python
# -*- coding: utf-8 -*-

from otwstest.schema.tree_of_life.induced_subtree import validate
from otwstest import all_api_versions, not_v2_version


@not_v2_version
def test_top(outcome):
    url = outcome.make_front_end_url('')
    outcome.do_http_json(url, return_raw_content=True)

@not_v2_version
def test_curator(outcome):
    url = outcome.make_front_end_url('curator')
    outcome.do_http_json(url, return_raw_content=True)


@not_v2_version
def test_contact(outcome):
    url = outcome.make_front_end_url('contact')
    outcome.do_http_json(url, return_raw_content=True)

@not_v2_version
def test_about(outcome):
    url = outcome.make_front_end_url('about')
    outcome.do_http_json(url, return_raw_content=True)

@not_v2_version
def test_references(outcome):
    url = outcome.make_front_end_url('about/references')
    outcome.do_http_json(url, return_raw_content=True)

