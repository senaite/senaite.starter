# -*- coding: utf-8 -*-

import doctest
from os.path import join
from os.path import splitext

import pkg_resources
import unittest2 as unittest
from Testing import ZopeTestCase as ztc

from .base import SimpleTestCase

FLAGS = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_NDIFF
PACKAGE_NAME = "senaite.starter"


def test_suite():
    suite = unittest.TestSuite()
    for doctest_file in get_doctest_files():
        suite.addTests([
            ztc.ZopeDocFileSuite(
                doctest_file,
                test_class=SimpleTestCase,
                optionflags=FLAGS
            )
        ])
    return suite


def get_doctest_files(path=""):
    """Returns a list with the doctest files
    """
    files = []
    resources = pkg_resources.resource_listdir(PACKAGE_NAME, path)
    for resource in resources:
        if pkg_resources.resource_isdir(PACKAGE_NAME, resource):
            files.extend(get_doctest_files(join(path, resource)))
        else:
            basename, ext = splitext(resource)
            if ext in [".md", ".rst", ".txt"]:
                files.append(join("..", path, resource))

    return files
