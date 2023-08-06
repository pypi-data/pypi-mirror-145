# -*- coding: utf-8 -*-

import codecs
try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

# usage:
# python setup.py bdist_wininst generate a window executable file
# python setup.py bdist_egg generate a egg file
# Release information about eway

description = "kivy charts is a tool to build kivy data plot"
author = "yumoqing"
email = "yumoqing@icloud.com"
version = '0.0.8'
depandent_packages = []
with codecs.open('./requirements.txt', 'r', 'utf-8') as f:
	b = f.read()
	b = ''.join(b.split('\r'))
	depandent_packages = b.split('\n')
print('########depandent_packages=', depandent_packages)

package_data = {
	"":[
		"*.txt"
	]
}

setup(
    name="kivycharts",
	ext_modules= [
		],
    version=version,
    
    # uncomment the following lines if you fill them out in release.py
    description=description,
    author=author,
    author_email=email,
   
    install_requires=depandent_packages,
    packages=[ 'kivycharts' ],
    package_data=package_data,
    keywords = [
    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
	platforms= 'any'
)
