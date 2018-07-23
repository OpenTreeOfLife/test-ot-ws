#!/usr/bin/env python
# -*- coding: utf-8 -*-

from otwstest.schema.tree_of_life.about import validate
from otwstest import all_api_versions


@all_api_versions
def test_simple(outcome):
    url = outcome.make_url('tree_of_life/about')
    outcome.do_http_json(url, 'POST',
                         data={"include_source_list": True},
                         validator=validate)
