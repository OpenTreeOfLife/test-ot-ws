# Open Tree integration tests

This repository holds integration tests, intended to answer the
question, is a new version of the web site good enough to go to
production?

## Installation (for end-users)

    python setup.py install


### tab-completion
Add:

    source {ABSPATH TO YOUR CLONE OF THIS REPO}/dev/completion.sh

to your `.bashrc` (or equivalent) to get tab completion of options for the `test-ot-ws`
script.

## Installation (for developers)
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

## History of this repo
This code was previously in the [germinator](https://github.com/OpenTreeOfLife/germinator)
    repository with the individual tests spread out across each of
    the implementation repositories and peyotl as a prerequisite.
The goal of this refactoring was for the test repository for integration tests
    to be standalone and easier to use.


