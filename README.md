# Open Tree integration tests

This repository holds integration tests, intended to answer the
question, is a new version of the web site good enough to go to
production?

# Installation 
Python 3.5 or higher is recommended (see note below on python2.7 prerequisites).

## For end-users:
Using a 
[virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
is probably a wise move (as it is for most work-in-progress python packages).

    python setup.py install


## Tab-completion
A bash script is included that provides pretty good tab-completion
 (including completion to finish arguments that select what test to run).
Since there are a lot of tests, it is quite handy to be able to run a subset
of them.
Add:

    source {ABSPATH TO YOUR CLONE OF THIS REPO}/dev/completion.sh

to your `.bashrc` (or equivalent) to get tab completion of options for the `test-ot-ws`
script.

## For developers:
One time only:

    virtualenv -p$(which python3) env
    source env/bin/activate
    python setup develop
    source dev/activate.sh

then add:

    source {ABSPATH TO YOUR CLONE OF THIS REPO}/env/bin/activate
    source {ABSPATH TO YOUR CLONE OF THIS REPO}/dev/activate.sh

to some script that you source whenever you want to run the tests.
Note that the `activate.sh` sources the `completion.sh`, so you won't need to do
    that step explicitly.

You may need to run

    pip install -r requirements.txt

if the prerequisites of the package change over time.

## Python 2.7 support
You'll need to run:

    pip install enum34

if you are using Python 2.7

# Usage
The `test-ot-ws` script is a Python program that tests aspects of the 
[v2](https://github.com/OpenTreeOfLife/opentree/wiki/Open-Tree-of-Life-APIs) and
[v3](https://github.com/OpenTreeOfLife/germinator/wiki/Open-Tree-of-Life-Web-APIs)
versions of the Open Tree of Life web APIs.
Details of the tests performed and the results are stored in a scratch directory
    at `~/.opentreeoflife/test-ot-ws`

## Services
The top-level services of the api are `studies`, `taxonomy`, `tnrs`,
    and `tree_of_life`.
Version 0.1.0 of the test software only supports tests of the `taxonomy` and
    `tnrs` services.
The default behavior is to test all of the services that are supported, but 
    you can specify positional arguments to limit this. 
So `test-ot-ws` runs all of the test, while `test-ot-ws tnrs` would just
    run the `tnrs` tests.

## Running a subset of tests
The `--test=` argument can be used to select a test or a subset of tests.
Either `--test=XYZ` or `--test=XYZ.` would cause any test that matches the
 [glob](https://en.wikipedia.org/wiki/Glob_(programming)) 
`XYZ.*` to be run.
Note that (at least in version 0.1.0 of the testing tool), the globbing
    only works at different levels of the test hierarchies (not within a
    word).
    
So, `test-ot-ws --test=tnrs.test_contexts.v3` would run a test of the
    `tnrs/contexts` API function in version 3 of the API, while
    `test-ot-ws --test=tnrs.test_contexts` would test that method under 
    both the 2 and 3 versions of the API.
 
## System to test
This is used to specify whether or not the tests run against:
  * `production` - calls methods on `https://api.opentreeoflife.org` and 
    does not support any tests that write
  * `dev` - calls methods on `https://devapi.opentreeoflife.org`. When 
    tests that write to databases are added to the repertoire, then
    these can be tried on dev (an additional `--allow-write` argument
    will also be added).
  * `local` - assumes that you are running the services locally using
    the default configuration. So:
    * `taxonomy` and `tnrs` tests run against URLs that start with
    `http://localhost:7474/db/data/ext/`

## API-version
The default is to test both `v2` and `v3` of the API, but either can 
be selected by using syntax similar to `--api-vesion=v3`.

## Actions
This argument controls the main action taken by the invocaton.

  * `test` is the default. This is used to run tests and exit with a return
  code that indicates the number of problems encountered. 
  * `retry-failing` runs only the subset of tests that have previously
  failed.
  * `report` describes the last run state of each test without 
  re-executing any tests.
  * `curl` writes the HTTP calls made in an already executed test out
  to standard output as a curl command.
  * `scan` is rarely (if ever) needed. This is only used by developers
  to records the list of available tests for better tab-completion. This
  list is autogenerated if a `--test=` argument fails, so it should not
  be necessary to run `scan`
  
## --version
reports the version of the testing tool.

## --noise=#
Specifies the the noisyness level from 0 (silent) up to 5 (tracing of
actions) 


## --threads=#
The number of threads to use when simultaneously running tests.
The default is 8. Large choices could overload the server, so be careful.


# History of this repo
This code was previously in the [germinator](https://github.com/OpenTreeOfLife/germinator)
    repository with the individual tests spread out across each of
    the implementation repositories and peyotl as a prerequisite.
The goal of this refactoring was for the test repository for integration tests
    to be standalone and easier to use.


