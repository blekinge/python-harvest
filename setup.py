import os

from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


requirements = [
    'requests',
    'requests_oauthlib',
    'typing',
    'inflection'
    # TODO: put package requirements here
]

test_requirements = [
    'pytest==2.9.2',
    'pytest-runner==2.8',
    # TODO: put package test requirements here
]

setup(
    name='statsbiblioteket.harvest',
    version='1.0.4',
    description="Harvest api client",
    long_description=read('README.md'),
    url='https://github.com/blekinge/python-harvest',
    author="Asger Askov Blekinge",
    author_email='asger.askov.blekinge@gmail.com',

    packages=[
        'statsbiblioteket.harvest',
    ],
    include_package_data=True,
    install_requires=requirements,

    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=['pytest-runner'],

    entry_points={
        "console_scripts": ['github_cloner = '
                            'statsbiblioteket.github_cloner.github_cloner'
                            ':main']
    },

    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    keywords='harvestapp timetracking api',
    license='MIT License',
    zip_safe=True,
)
