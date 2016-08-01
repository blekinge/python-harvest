from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['requests', 'requests_oauthlib', 'typing', 'inflection',
    'sqlalchemy', 'argparse', 'python_log_indenter']

test_requirements = ['pytest', 'pytest-runner',]

setup(name='statsbiblioteket.harvest',
      version='1.1.3rc',
        description="Harvest api client", long_description=readme,
        url='https://github.com/statsbiblioteket/python-harvest',
        author="Asger Askov Blekinge",
        author_email='asger.askov.blekinge@gmail.com',

        packages=['statsbiblioteket.harvest', ],
        include_package_data=True,
        install_requires=requirements,

        test_suite='tests',
        tests_require=test_requirements,
        setup_requires=['pytest-runner'],

        entry_points={"console_scripts": ['harvest = '
                                          'statsbiblioteket.harvest.synch.harvest_synch'
                                          ':main']},

        # http://pypi.python.org/pypi?:action=list_classifiers
        classifiers=["Development Status :: 5 - Production/Stable",
            "Environment :: Console", "Intended Audience :: Developers",
            "Natural Language :: English",
            "Operating System :: POSIX :: Linux",
            "Programming Language :: Python :: 3.5",
            "Topic :: Software Development :: Libraries",
            "Topic :: Internet :: WWW/HTTP :: Site Management",
            "Topic :: Utilities", "License :: OSI Approved :: MIT License", ],
        keywords='harvestapp timetracking api', license='MIT License',
        zip_safe=False,
      )
