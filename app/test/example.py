"""
	An example test suite
	~~~~~~~~~~~~~~~~~~~~~

	Based on Armin Ronacher's Werkzeug tests
"""

import os
import time
import unittest
import tempfile
import shutil

from app.test import TestMain

class SimpleTestCase(TestMain):

	def test_something(self):
		assert True

def suite():
	"""
	It's vital that you have this function - the test loader looks 
	for an object with this name and then calls it to load the tests
	"""

	suite = unittest.TestSuite()
	suite.addTest(unittest.makeSuite(SimpleTestCase))

	# you can do conditional adds as well - this can be as dirty as you'd like
	return suite