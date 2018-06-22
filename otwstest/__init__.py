#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import types
import traceback
from enum import Enum

from . import taxonomy


def run_tests(test_config, addr_fn_pairs_list, test_results):
    good = True
    for test_addr, fn in addr_fn_pairs_list:
        good = test_config.run_test(test_addr=test_addr,
                                    test_func=fn,
                                    test_results=test_results) and good
    return good

class TestStatus(Enum):
    """Status integer used by TestOutcome instances"""
    RUNNING = 0
    SUCCESS = 1
    FAILED = 2
    ERROR = 3
    SKIPPED = 4
    UNCAUGHT_EXCEPTION = 5  # error not caught by test function

class TestResults(object):
    def __init__(self):
        self._run = []
        self._succeeded = []
        self._errored = []
        self._failed = []
        self._skipped = []
        self._exceptions_uncaught = []
        self._spawned_unfinished = set()
        self._status2list = {TestStatus.SUCCESS: self._succeeded,
                             TestStatus.ERROR: self._errored,
                             TestStatus.FAILED: self._failed,
                             TestStatus.SKIPPED: self._skipped,
                             TestStatus.UNCAUGHT_EXCEPTION: self._exceptions_uncaught,
                             }

    def _reg_as_finished(self, outcome):
        self._run.append(outcome)
        try:
            self._spawned_unfinished.remove(outcome)
        except Exception:
            pass

    def register(self, outcome):
        self._reg_as_finished(outcome)
        self._status2list[outcome.status].append(outcome)

    @property
    def num_problems(self):
        return sum([len(i) for i in (self._failed, self._errored, self._exceptions_uncaught)])

    # noinspection PyUnusedLocal
    def spawning_test(self, config, test_addr):
        tout = TestOutcome(self, test_addr)
        self._spawned_unfinished.add(tout)
        return tout


class TestOutcome(object):
    def __init__(self, results_obj, test_addr):
        self.test_addr = test_addr
        self.status = TestStatus.RUNNING
        self._results_collection = results_obj
        self._data = {}

    @property
    def succeeded(self):
        return self.status == TestStatus.SUCCESS

    def __hash__(self):
        return hash(self.test_addr)

    def uncaught(self, ex_message):
        self.status = TestStatus.UNCAUGHT_EXCEPTION
        self._data['exception'] = ex_message

    def _finalize(self):
        if self.status == TestStatus.RUNNING:
            self.status = TestStatus.SUCCESS

    def record(self, config):
        self._finalize()
        if self._results_collection:
            self._results_collection.register(self)


SYST_CHOICES = frozenset(['production', 'dev', 'local'])


class TestingConfig(object):
    def __init__(self, system_to_test, noise_level=2):
        self.system_to_test = system_to_test.lower()
        assert self.system_to_test in SYST_CHOICES
        self.noise_level = noise_level

    def as_arg_list(self):
        a = ['--system={}'.format(self.system_to_test),
             '--noise={}'.format(self.noise_level),
            ]
        return a

    def run_test(self, test_addr, test_func, test_results):
        outcome = test_results.spawning_test(self, test_addr)
        try:
            test_func(self, outcome)
        except Exception:
            outcome.uncaught(traceback.format_exc())
        outcome.record(self)
        return outcome.succeeded


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

def _aug_comp_list_eq(opts_to_values, key, comp_list):
    vals = opts_to_values.get(key, [])
    comp_list.extend(['{}={}'.format(key, i) for i in vals])

def _aug_comp_list_eq_started(opts_to_values, key, val_start, comp_list):
    vals = opts_to_values.get(key, [])
    if val_start in vals:
        return True
    comp_list.extend([i for i in vals if i.startswith(val_start)])
    return False

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
    p.add_argument("--noise",
                   default=2,
                   type=int,
                   required=False,
                   help='Controls level of output sent to standard error: 0=silent, ' \
                        '1=only numbers of outcomes, 2(default)=progress and outcomes, '\
                        '3=brief message for each failure, 4=detailed messages, '\
                        '5=trace level')

    p.add_argument('--system', choices=SYST_CHOICES, default='production')
    serv_choices = ('taxonomy',)
    if deleg is None:
        p.add_argument('service', nargs='?', choices=serv_choices)
    tr = TestResults()
    if "--show-completions" in argv:
        try:
            a = argv[3:]
        except Exception:
            a = []
        # sys.stderr.write('\na={}\n'.format(a))
        opts_to_values = {'--system': SYST_CHOICES,
                          '--noise': [str(i) for i in range(6)],
                          }
        comp_list = []
        ov_end = len(a) == 0
        if not ov_end:
            last = a[-1]
            if last.startswith('-'):
                # completing an option
                assert '=' not in last
                for key, vals in opts_to_values.items():
                    if key.startswith(last) and key not in a:
                        comp_list.extend(['{}={}'.format(key, i) for i in vals])
            elif last == '=':
                # = sign separating an option from its value.
                if len(a) > 1:
                    _aug_comp_list_eq(opts_to_values, a[-2], comp_list)
            elif len(a) > 2 and a[-2] == '=':
                # complete a the value in progress
                if _aug_comp_list_eq_started(opts_to_values, a[-3], last, comp_list):
                    ov_end = True
            else:
                for s in serv_choices:
                    if s.startswith(last):
                        if s == last:
                            ov_end = True
                            break
                        else:
                            comp_list.append(s)
        if ov_end:
            for s in serv_choices:
                if s not in a:
                    comp_list.append(s)
            for o in opts_to_values.keys():
                if o not in a:
                    comp_list.append(o)
        sys.stdout.write('{}\n'.format(' '.join(comp_list)))
        # sys.stderr.write('\nfinal return: {}\n'.format(' '.join(comp_list)))
        return tr
    parsed = p.parse_args(args=argv[1:])
    tc = TestingConfig(system_to_test=parsed.system,
                       noise_level=parsed.noise)
    if deleg is None:
        # noinspection PyUnresolvedReferences
        import otwstest
        s = parsed.service
        if isinstance(s, str):
            s = [s]
        services = list(s or serv_choices)
        services.sort()
        addr = 'otwstest.'
        file_func_pairs = []
        for s in services:
            file_func_pairs.extend(_collect_file_func_pairs(otwstest.__dict__[s], addr + s))
        run_tests(tc, file_func_pairs, tr)
    return tr
