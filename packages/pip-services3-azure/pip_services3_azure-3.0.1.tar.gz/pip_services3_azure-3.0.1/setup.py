"""
Pip.Services Azure
--------------------

Pip.Services is an open-source library of basic microservices.
pip_services3_azure package provides Azure specific components for Python.

Links
`````

* `website <http://github.com/pip-services/pip-services>`
* `development version <http://github.com/pip-services-python/pip-services-azure-python>`

"""

from setuptools import find_packages
from setuptools import setup

try:
    readme = open('readme.md').read()
except:
    readme = __doc__

setup(
    name='pip_services3_azure',
    version='3.0.1',
    url='http://github.com/pip-services3-python/pip-services3-azure-python',
    license='MIT',
    description='',
    author='Conceptual Vision Consulting LLC',
    author_email='seroukhov@gmail.com',
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=['config', 'data', 'test']),
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    install_requires=[
        'azure-functions >= 1.8.0, < 2.0.0',

        'pip_services3_commons >= 3.3.12, < 4.0.0',
        'pip_services3_components >= 3.5.9, < 4.0.0',
        'pip_services3_container >= 3.2.5, < 4.0.0',
        'pip_services3_rpc >= 3.3.2, < 4.0.0'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
