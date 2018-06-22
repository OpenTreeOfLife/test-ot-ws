#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import types

from . import taxonomy


def run_test(test_config, test_addr, test_func, test_results):
    """Core"""
    try:
        if test_func(test_config, test_addr, test_results):
            return True
    except Exception:
        test_results.flag_uncaught(test_addr)
    return False

def run_tests(test_config, addr_fn_pairs_list, test_results):
    good = True
    for test_addr, fn in addr_fn_pairs_list:
        good = run_test(test_config,
                        test_addr=test_addr,
                        test_func=fn,
                        test_results=test_results) and good
    return good



class TestResults(object):
    def __init__(self):
        self._run = []
        self._skipped = []
        self._failures = []
        self._errors = []
        self._exceptions_uncaught = []

    def flag_uncaught(self, addr):
        self._exceptions_uncaught.append(addr)

    @property
    def num_problems(self):
        return sum([len(i) for i in (self._failures, self._errors, self._exceptions_uncaught)])


SYST_CHOICES = frozenset(['production', 'dev', 'local'])


class TestingConfig(object):
    def __init__(self, system_to_test, verbose=False):
        self.system_to_test = system_to_test.lower()
        assert self.system_to_test in SYST_CHOICES
        self.verbose = verbose

    def as_arg_list(self):
        a = ['--system={}'.format(self.system_to_test)]
        if self.verbose:
            a.append('--verbose')
        return a


def _collect_file_func_pairs(mod_obj, addr):
    ret = []
    for k, v in mod_obj.__dict__.items():
        if k.startswith('_'):
            continue
        extended = '{}.{}'.format(addr, k)
        if k.startswith('test'):
            ret.append((extended, v))
        elif isinstance(v, types.ModuleType):
            ret.extend(_collect_file_func_pairs(v, extended))
    return ret


def top_main(argv, deleg=None):
    import argparse
    description = "Tests of web services for Open Tree of Life project"
    if deleg is not None:
        description += ' tests just from "{}"'.format(deleg)
    p = argparse.ArgumentParser(description=description)
    p.add_argument("--show-completions",
                   action="store_true",
                   default=False,
                   help=argparse.SUPPRESS)
    p.add_argument("--verbose",
                   action="store_true",
                   default=False,
                   help='produce more output to standard error.')

    p.add_argument('--system', choices=SYST_CHOICES, default='production')
    serv_choices = ('taxonomy',)
    if deleg is None:
        p.add_argument('service', nargs='?', choices=serv_choices)
    tr = TestResults()
    if "--show-completions" in argv:
        a = argv[1:]
        # sys.stderr.write('a = {}\n'.format(a))
        comp_list = []
        tc_syst_choices = []
        try:
            syst_ind = a.index('--system')
        except ValueError:
            tc_syst_choices = ['--system={}'.format(i) for i in SYST_CHOICES]
        else:
            if syst_ind + 1 < len(a) and a[1 + syst_ind] == '=':
                if syst_ind + 3 == len(a):
                    for c in SYST_CHOICES:
                        if c.startswith(a[-1]) and c != a[-1]:
                            tc_syst_choices.append(c)
                elif syst_ind + 2 >= len(a):
                    tc_syst_choices = SYST_CHOICES
        comp_list.extend(tc_syst_choices)
        if deleg is None:
            if a[-1] != '=' and not a[-1].startswith('-'):
                for s in serv_choices:
                    if s not in a:
                        comp_list.append(s)
        sys.stdout.write('{}\n'.format(' '.join(comp_list)))
        # sys.stderr.write('\n{}\n'.format(' '.join(comp_list)))
        return tr
    parsed = p.parse_args(args=argv[1:])
    tc = TestingConfig(system_to_test=parsed.system,
                       verbose=parsed.verbose)
    if deleg is None:
        # noinspection PyUnresolvedReferences
        import otwstest
        services = list(parsed.service or serv_choices)
        services.sort()
        addr = 'otwstest.'
        file_func_pairs = []
        for s in services:
            file_func_pairs.extend(_collect_file_func_pairs(otwstest.__dict__[s], addr + s))
        run_tests(tc, file_func_pairs, tr)
    return tr
