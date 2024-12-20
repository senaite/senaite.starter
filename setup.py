# -*- coding: utf-8 -*-

from os.path import join
from os.path import dirname
from setuptools import setup, find_packages

version = "1.0.0"

with open(join(dirname(__file__), "docs", "README.md")) as f:
    long_description = f.read()

with open(join(dirname(__file__), "docs", "CHANGES.md")) as f:
    long_description += "\n\n"
    long_description += f.read()


setup(
    name="senaite.starter",
    version=version,
    description="An installable SENAITE LIMS extension for individual customization purposes",
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords=["senaite", "lims"],
    author="Ramon Bartl",
    author_email="rb@ridingbytes.com",
    url="ridingbytes/senaite.starter",
    license="GPLv2",
    packages=find_packages("src"),
    package_dir={"": "src"},
    namespace_packages=["senaite"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "senaite.lims",
        "setuptools",
    ],
    extras_require={
        "test": [
            "Products.PloneTestCase",
            "Products.SecureMailHost",
            "plone.app.testing",
            "unittest2",
        ]
    },
    entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
