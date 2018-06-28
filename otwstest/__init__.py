#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import sys
import types
import traceback
import codecs
import json
try:
    from enum import Enum
except:
    from enum34 import Enum
import requests
import jsonschema

if sys.version_info.major == 2:
    # noinspection PyUnresolvedReferences
    def is_str_type(x):
        # noinspection PyCompatibility
        return isinstance(x, basestring)
else:
    def is_str_type(x):
        return isinstance(x, str)


def run_tests(test_config, addr_fn_pairs_list, test_results):
    good = True
    for test_addr, fn in addr_fn_pairs_list:
        good = test_config.run_test(test_addr=test_addr,
                                    test_func=fn,
                                    test_results=test_results) and good
    return good


def write_as_json(blob, dest, indent=0, sort_keys=True):
    """Writes `blob` as JSON to the filepath `dest` or the filestream `dest` (if it isn't a string)
    uses utf-8 encoding if the filepath is given (does not change the encoding if dest is already open).
    """
    opened_out = False
    if is_str_type(dest):
        out = codecs.open(dest, mode='w', encoding='utf-8')
        opened_out = True
    else:
        out = dest
    try:
        if indent == 0:
            json.dump(blob, out, indent=indent, sort_keys=sort_keys)
        else:
            json.dump(blob, out, indent=indent, sort_keys=sort_keys, separators=(',', ': '))
        out.write('\n')
    finally:
        out.flush()
        if opened_out:
            out.close()


class TestStatus(Enum):
    """Status integer used by TestOutcome instances"""
    RUNNING = 0
    SUCCESS = 1
    FAILED = 2
    ERROR = 3
    SKIPPED = 4
    UNCAUGHT_EXCEPTION = 5  # error not caught by test function


STATUS_TO_SINGLE_LTR = {TestStatus.SUCCESS: '.',
                        TestStatus.ERROR: 'E',
                        TestStatus.FAILED: 'f',
                        TestStatus.SKIPPED: 's',
                        TestStatus.UNCAUGHT_EXCEPTION: 'X',
                        }


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

    def flush(self, context):
        if context.noise_level >= 1 and len(self._run) > 0:
            m = '\n{} test(s) run. {} succeeded. {} failed. {} errored. {} skipped. ' \
                '{} raised exceptions.   {}/{} success rate.'
            m = m.format(len(self._run), len(self._succeeded), len(self._failed),
                         len(self._errored), len(self._skipped), len(self._exceptions_uncaught),
                         len(self._succeeded), len(self._run) - len(self._skipped))
            context.status_message(1, m)

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
        tout = TestOutcome(self, test_addr, config)
        self._spawned_unfinished.add(tout)
        return tout


class TestOutcome(object):
    def __init__(self, results_obj, test_addr, config):
        self.test_addr = test_addr
        self.config = config
        self.status = TestStatus.RUNNING
        self._results_collection = results_obj
        self._data = {}
        self.brief, self.detailed = '', ''

    def store(self, key, value):
        self._data[key] = value

    def get(self, key, default):
        return self._data.setdefault(key, default)

    @property
    def succeeded(self):
        return self.status == TestStatus.SUCCESS

    def __hash__(self):
        return hash(self.test_addr)

    def uncaught(self, ex_message):
        self.status = TestStatus.UNCAUGHT_EXCEPTION
        self.store('exception', ex_message)

    def _finalize(self):
        if self.status == TestStatus.RUNNING:
            self.status = TestStatus.SUCCESS

    def record(self, config):
        self._finalize()
        if self._results_collection:
            self._results_collection.register(self)
        self.serialize(config)
        config.status_message(2, STATUS_TO_SINGLE_LTR[self.status])
        if self.status != TestStatus.SUCCESS and config.noise_level > 2:
            if config.noise_level == 3:
                self.brief_diagnosis(config)
            else:
                self.full_diagnosis(config)

    def brief_diagnosis(self, config):
        m = None
        if self.status == TestStatus.UNCAUGHT_EXCEPTION:
            m = 'Exception not handled by test function (please report this error)'
        elif self.status != TestStatus.SUCCESS:
            m = '{}. {}'.format(_tstatus_to_str(self.status), self.brief)
        if m:
            config.status_message(3, '{}: {}\n'.format(self.test_addr, m))

    def full_diagnosis(self, config):
        m = None
        if self.status == TestStatus.UNCAUGHT_EXCEPTION:
            m = 'Exception not handled by test function (please report this error).\nException:\n'
            m += self._data['exception']
        elif self.status != TestStatus.SUCCESS:
            m = '{}. {}'.format(_tstatus_to_str(self.status), self.detailed)
        if m:
            config.status_message(4, '{}: {}\n'.format(self.test_addr, m))

    def serialize(self, config):
        results_dir = config.get_results_dir(self.test_addr)
        outf = os.path.join(results_dir, 'outcome.json')
        self.store('status', _tstatus_to_str(self.status))
        self.store('test_addr', self.test_addr)
        write_as_json(self._data, outf, indent=2)

    # noinspection PyMethodMayBeStatic
    def raise_for_status(self, resp):
        try:
            resp.raise_for_status()
        except Exception as e:
            try:
                j = resp.json()
                m = '\n    '.join(['"{k}": {v}'.format(k=k, v=v) for k, v in j.items()])
                sys.stderr.write('resp.json = {t}'.format(t=m))
            except Exception:
                if resp.text:
                    sys.stderr.write('resp.text = {t}\n'.format(t=resp.text))
            raise e

    def do_http_json(self,
                     url,
                     verb='GET',
                     data=None,
                     headers=None,
                     expected_status=200,
                     expected_response=None,
                     schema=None,
                     validator=None):
        """Call `url` with the http method of `verb`.
        If specified `data` is passed using json.dumps
        returns True if the response:
             has the expected status code, AND
             has the expected content (if expected_response is not None)
        """
        if headers is None:
            headers = {'content-type': 'application/json', 'accept': 'application/json', }
        resp, call_out = self.request(verb, url, headers, data=data)
        call_out['expected_status_code'] = expected_status
        if resp.status_code != expected_status:
            m = 'Wrong status code. Expected {}. Got {}.'.format(resp.status_code, expected_status)
            self.set_error(m)
            return None
        results = resp.json()
        call_out['response_body'] = results
        if schema is not None or validator is not None:
            try:
                if schema is not None:
                    jsonschema.validate(results, schema)
                if validator is not None:
                    validator(results)
            except jsonschema.ValidationError as x:
                m = 'Invalid response body. Validator says: {}'.format(str(x))
                self.set_error(m)

        if expected_response is not None:
            if results != expected_response:
                call_out['expected_response_body'] = expected_response
                m = 'Wrong response body. Expected {}. Got {}.'.format(results, expected_response)
                self.set_error(m)
                return None
        return results

    def request(self, verb, url, headers, data=None):
        call_out = self.get('calls', [])
        stored = {'url': url, 'verb': verb, 'headers': headers, 'data': data}
        call_out.append(stored)
        if data:
            resp = requests.request(verb,
                                    url,
                                    headers=headers,
                                    data=json.dumps(data),
                                    allow_redirects=True)
        else:
            resp = requests.request(verb,
                                    url,
                                    headers=headers,
                                    allow_redirects=True)
        stored['status_code'] = resp.status_code
        debug('Sent {v} to {s}\n'.format(v=verb, s=resp.url))
        return resp, stored

    def set_error(self, brief, detailed=None):
        self.status = TestStatus.ERROR
        self.brief = brief
        self.detailed = detailed if detailed else brief


def _tstatus_to_str(status):
    return str(status)[len('TestStatus.'):]


SYST_CHOICES = frozenset(['dev', 'local', 'production', ])
ACTION_CHOICES = frozenset(['retry-failing', 'scan', 'test', ])
SCRIPT_NAME = os.path.split(sys.argv[0])[-1]
DEBUG_OUTPUT = False
TEST_CACHE_PAR = os.path.expanduser('~/.opentreeoflife/test-ot-ws')
TEST_ADDR_LIST = os.path.join(TEST_CACHE_PAR, 'test_addr.json')
SERVICE_CHOICES = ('taxonomy',)


def debug(msg):
    if DEBUG_OUTPUT:
        sys.stderr.write('{} debug: {}\n'.format(SCRIPT_NAME, msg))


def write_test_list_to_store(iterable):
    write_as_json(iterable, TEST_ADDR_LIST, indent=2)


def read_test_list_from_store():
    if not os.path.exists(TEST_ADDR_LIST):
        return []
    return json.load(codecs.open(TEST_ADDR_LIST, 'rU', encoding='utf-8'))


def get_full_test_list():
    x = read_test_list_from_store()
    if not x:
        # noinspection PyTypeChecker
        x = [i[0] for i in scan_for_services(SERVICE_CHOICES)]
    pref = 'otwstest.'
    lp = len(pref)
    return [i[lp:] if i.startswith(pref) else i for i in x]


def scan_for_services(services):
    if not isinstance(services, list):
        services = list(services)
    services.sort()
    addr = 'otwstest.'
    file_func_pairs = []
    # noinspection PyUnresolvedReferences
    import otwstest
    for s in services:
        file_func_pairs.extend(_collect_file_func_pairs(otwstest.__dict__[s], addr + s))
    return file_func_pairs


class TestingConfig(object):
    def __init__(self, system_to_test, noise_level=2):
        global DEBUG_OUTPUT
        self.system_to_test = system_to_test.lower()
        assert self.system_to_test in SYST_CHOICES
        self.noise_level = noise_level
        if self.noise_level >= 5:
            DEBUG_OUTPUT = True
        self.needs_newline = False
        self._res_par = os.path.join(TEST_CACHE_PAR, system_to_test)

    def get_results_dir(self, addr):
        cull_pref = 'otwstest.'
        if addr.startswith(cull_pref):
            addr = addr[len(cull_pref):]
        addr = '/'.join(addr.split('.'))
        res_dir = os.path.join(self._res_par, addr)
        if not os.path.exists(res_dir):
            os.makedirs(res_dir)
        return res_dir

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

    def status_message(self, level, message):
        if self.noise_level >= level:
            sys.stderr.write(message)
            self.needs_newline = not message.endswith('\n')

    def flush(self, results):
        results.flush(self)
        if self.needs_newline:
            sys.stderr.write('\n')

    def make_url(self, frag):
        while frag.startswith('/'):
            frag = frag[1:]
        while frag.endswith('/'):
            frag = frag[:-1]
        if self.system_to_test == 'production':
            return 'https://api.opentreeoflife.org/{}'.format(frag)
        if self.system_to_test == 'dev':
            return 'https://devapi.opentreeoflife.org/{}'.format(frag)
        raise NotImplemented('local system_to_test')

    def iter_previous(self):
        if not os.path.exists(self._res_par):
            return
        for d, sub, file_list in os.walk(self._res_par):
            for fn in file_list:
                if fn == 'outcome.json':
                    yield json.load(codecs.open(os.path.join(d, fn), 'rU', encoding='utf-8'))


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
    vals = list(opts_to_values.get(key, []))
    vals.sort()
    # sys.stderr.write('\nkey = {} vals={}\n'.format(key, vals))
    comp_list.extend(['{}'.format(i) for i in vals])


def _aug_comp_list_eq_started(opts_to_values, key, val_start, comp_list):
    vals = opts_to_values.get(key, [])
    if val_start in vals:
        return True
    vals = list(vals)
    vals.sort()
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
                   help='Controls level of output sent to standard error: 0=silent, '
                        '1=only numbers of outcomes, 2(default)=progress and outcomes, '
                        '3=brief message for each failure, 4=detailed messages, '
                        '5=trace level')

    p.add_argument('--action', choices=ACTION_CHOICES, default='test')
    p.add_argument('--system', choices=SYST_CHOICES, default='production')
    TEST_CHOICES = get_full_test_list()
    p.add_argument('--test', choices=TEST_CHOICES, default=None, required=False)

    if deleg is None:
        p.add_argument('service', nargs='?', choices=SERVICE_CHOICES)
    tr = TestResults()
    if "--show-completions" in argv:
        try:
            a = argv[3:]
        except Exception:
            a = []
        # sys.stderr.write('\na={}\n'.format(a))
        opts_to_values = {'--noise': [str(i) for i in range(6)],
                          '--actions': ACTION_CHOICES,
                          '--system': SYST_CHOICES,
                          '--test': TEST_CHOICES,
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
                for s in SERVICE_CHOICES:
                    if s.startswith(last):
                        if s == last:
                            ov_end = True
                            break
                        else:
                            comp_list.append(s)
        if ov_end:
            for s in SERVICE_CHOICES:
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
    try:
        if deleg is None:
            # noinspection PyUnresolvedReferences
            s = parsed.service
            if isinstance(s, str):
                s = [s]
            file_func_pairs = scan_for_services(list(s or SERVICE_CHOICES))
            addr_to_skip = []
            if parsed.action == 'retry-failing':
                for blob in tc.iter_previous():
                    if blob.get('status', '').upper() == 'SUCCESS':
                        addr_to_skip.append(blob['test_addr'])
            elif parsed.action == 'scan':
                write_test_list_to_store([i[0] for i in file_func_pairs])
                sys.exit(0)
            addr_to_skip = frozenset(addr_to_skip)
            file_func_pairs = [i for i in file_func_pairs if i[0] not in addr_to_skip]
            if parsed.test is not None:
                try:
                    file_func_pairs = [i for i in file_func_pairs if i[0].endswith(parsed.test)]
                except Exception:
                    pass
                if len(file_func_pairs) == 0:
                    sys.exit('No tests matched --test="{}"'.format(parsed.test))
            run_tests(tc, file_func_pairs, tr)
        return tr
    finally:
        tc.flush(tr)

from . import taxonomy, schema

