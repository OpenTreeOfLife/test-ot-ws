#!/usr/bin/env python
# -*- coding: utf-8 -*-

from otwstest import all_api_versions


@all_api_versions
def test_get_tree_nexus(outcome):
    url = outcome.make_url('study/10/tree/tree3.nex')
    c = outcome.do_http_json(url, return_raw_content=True)
    if not c:
        outcome.exit_test_with_failure('no tree returned')
    if not c.startswith('#NEXUS'):
        outcome.exit_test_with_failure('.nex response did not starts with "#NEXUS"')


@all_api_versions
def test_get_tree_newick(outcome):
    url = outcome.make_url('study/10/tree/tree3.tre')
    c = outcome.do_http_json(url, return_raw_content=True)
    if not c:
        outcome.exit_test_with_failure('no tree returned')
    if not c.startswith('('):
        outcome.exit_test_with_failure('newick response did not starts with "("')


@all_api_versions
def test_get_tree(outcome):
    url = outcome.make_url('study/10/tree/tree3.tre')
    c = outcome.do_http_json(url, data={'bracket_ingroup': True},
                             return_raw_content=True)
    if not c:
        outcome.exit_test_with_failure('no tree returned')
    if not c.startswith('('):
        outcome.exit_test_with_failure('newick response did not starts with "("')
    if '[pre-ingroup-marker]' not in c:
        outcome.exit_test_with_failure('Requested "[pre-ingroup-marker]" was not in newick response')
