#!/usr/bin/env python
"""
    TestLoader
    ~~~~~~~~~~~~~~~~~~

    This file is a stripped down version of the Werkzeug test loader from the excellent Armin Ronacher
"""
from __future__ import with_statement

import pdb
import unittest
import random

import re
import sys
import unittest
import shutil
import tempfile
import atexit

from app.test.util import import_string, find_modules

from app import app, db
from app.main.models import *

"""
Utility functions to set up the testing suite
"""

def iter_suites(package):
    """Yields all testsuites."""
    for module in find_modules(package, include_packages=True):
        mod = __import__(module, fromlist=['*'])
        if hasattr(mod, 'suite'):
            yield mod.suite()


def find_all_tests(suite):
    """Yields all the tests and their names from a given suite."""
    suites = [suite]
    while suites:
        s = suites.pop()
        try:
            suites.extend(s)
        except TypeError:
            yield s, '%s.%s.%s' % (
                s.__class__.__module__,
                s.__class__.__name__,
                s._testMethodName
            )

class TestMain(unittest.TestCase):
    """
    A base class to inherit from, if you'd like

    This is much smaller than Armin's, but I thought it best to keep this uncluttered
    """

    # overwrite these on inheritance
    def setup(self):
        pass

    def teardown(self):
        pass

    # these are what actually gets executed
    def setUp(self):
        # app.config.from_object('testing_configuration') # put in a testing configuration
        db.session.close()
        db.drop_all()
        db.create_all()

        # do subclass setup
        self.setup()

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        self.teardown()

class BetterLoader(unittest.TestLoader):
    """A nicer loader that solves two problems.  First of all we are setting
    up tests from different sources and we're doing this programmatically
    which breaks the default loading logic so this is required anyways.
    Secondly this loader has a nicer interpolation for test names than the
    default one so you can just do ``run-tests.py ViewTestCase`` and it
    will work.
    """

    def getRootSuite(self):
        return suite()

    def loadTestsFromName(self, name, module=None):
        root = self.getRootSuite()
        if name == 'suite':
            return root

        all_tests = []
        for testcase, testname in find_all_tests(root):
            if testname == name or \
               testname.endswith('.' + name) or \
               ('.' + name + '.') in testname or \
               testname.startswith(name + '.'):
                all_tests.append(testcase)

        if not all_tests:
            raise LookupError('could not find test case for "%s"' % name)

        if len(all_tests) == 1:
            return all_tests[0]
        rv = unittest.TestSuite()
        for test in all_tests:
            rv.addTest(test)
        return rv

def suite():
    """A testsuite that has all the Flask tests.  You can use this
    function to integrate the Flask tests into your own testsuite
    in case you want to test that monkeypatches to Flask do not
    break it.
    """
    # patch it to work here
    package_def = 'app.test'

    suite = unittest.TestSuite()

    for other_suite in iter_suites(package_def):
        suite.addTest(other_suite)
    return suite

def main():
    """Runs the testsuite as command line application."""
    try:
        unittest.main(testLoader=BetterLoader(), defaultTest='suite')
    except Exception:
        import sys
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    print(__name__)
    main()