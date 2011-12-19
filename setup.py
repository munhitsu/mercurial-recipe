#!/usr/bin/env python

from setuptools import setup

setup(
	name = 'MercurialRecipe',
	version = '0.1.4a',
	description = 'zc.buildout recipe for cloning and/or pulling a Mercurial repository',
	author = 'Tim Molendijk',
	author_email = 'tim@timmolendijk.nl',
	url = 'http://bitbucket.org/tawm/mercurial-recipe/',
	packages = ['mercurialrecipe'],
	install_requires = ['Mercurial'],
	entry_points = {'zc.buildout': ['default = mercurialrecipe:Recipe']},
	classifiers = [
		'Development Status :: 3 - Alpha',
		'Environment :: Plugins',
		'Framework :: Buildout',
		'Intended Audience :: Developers',
		'Intended Audience :: System Administrators',
		'License :: OSI Approved',
		'Natural Language :: English',
		'Programming Language :: Python',
		'Topic :: Software Development :: Version Control',
	],
	zip_safe = True,
)
