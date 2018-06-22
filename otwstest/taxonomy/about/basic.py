#!/usr/bin/env python

def tests(config, outcome):
    url = config.make_url('v2/taxonomy/about')
    outcome.do_http_json(url, 'POST', expected_status=200)
    '''if not test:
        sys.exit(1)
    if u'source' not in result:
        sys.stderr.write('No source reported in \n{}'.format(result))
    sys.exit(1)
    if u'author' not in result:
        sys.stderr.write('No author reported in \n{}'.format(result))
    sys.exit(1)
    if u'weburl' not in result:
        sys.stderr.write('No weburl reported in \n{}'.format(result))
    sys.exit(1)

    print('hi')


'''