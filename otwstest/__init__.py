import os
import sys

SYST_CHOICES = frozenset(['production', 'dev', 'local'])
SCRIPT_DIR = os.path.abspath(os.path.dirname(sys.argv[0]))
NUM_FAILURES = 0


class TestResults(object):
    def __init__(self):
        self.num_tests_run = 0
        self.num_tests_skipped = 0
        self.num_failures = 0
        self.num_errors = 0
        self.num_exceptions_not_caught_by_test = 0

    def flag_uncaught(self):
        self.num_exceptions_not_caught_by_test += 1


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


def run_test(test_config, test_func, test_results):
    try:
        if test_func(test_config, test_results):
            return True
    except Exception:
        test_results.flag_uncaught()
    return False


def run_tests(test_config, srcfile_fn_pairs_list, test_results):
    good = True
    for srcfn, fn in srcfile_fn_pairs_list:
        good = run_test(test_config, test_func=fn, test_results=test_results) and good
    return good


def delegated_main(args, src_file, test_fn):
    top_main(args, deleg_file=src_file, deleg_fn=test_fn)


def top_main(argv, deleg_file=None, deleg_fn=None):
    global NUM_FAILURES
    import argparse
    description = "Tests of web services for Open Tree of Life project"
    if deleg_file is not None:
        description += ' tests just from "{}"'.format(deleg_file)
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
    if deleg_file is None:
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
        if deleg_file is None:
            if a[-1] != '=' and not a[-1].startswith('-'):
                for s in serv_choices:
                    if s not in a:
                        comp_list.append(s)
        sys.stdout.write('{}\n'.format(' '.join(comp_list)))
        # sys.stderr.write('\n{}\n'.format(' '.join(comp_list)))
    else:
        parsed = p.parse_args(args=argv[1:])
        tc = TestingConfig(system_to_test=parsed.system,
                           verbose=parsed.verbose)
        '''
        if deleg_file is None:
            services = list(parsed.service or serv_choices)
            services.sort()
            for s in services:
                for top_dir, sub_d_list, filename_list in os.walk(os.path.join(SCRIPT_DIR, s)):
                    for fn in filename_list:
                        if fn.startswith('test_') and fn.endswith('.py'):
                            fp = os.path.join(top_dir, fn)
                            print('fp="{}"'.format(fp))
                            invoc = [sys.executable, fp] + tc.as_arg_list()
                            print('invoc = {}'.format(invoc))
                            rc = subprocess.call(invoc)
                            NUM_FAILURES += rc
        else:
            file_fn_list = [(deleg_file, deleg_fn)]
            run_tests(tc, file_fn_list)
        '''
    return tr
