from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='loopcms',
    version='0.9.0',
    description='Loop CMS',
    long_description=long_description,
    url='https://github.com/MotherNatureNetwork/MNN',
    author='The Mother Nature Network Team',
    author_email='technical@mnn.com',
    license='Other/Proprietary',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='cms django',
    platforms=['OS Independent'],

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    # List run-time dependencies here.  These will be installed by pip when your
    # project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'Django==1.7.4',
        'Pillow==2.4.0',
        'boto==2.32.1',
        'celery==3.1.16',
        'django-compressor==1.4',
        'django-suit-redactor==0.0.2',
        'django-reversion==1.8.1',
        'django-storages==1.1.8',
        'django-watson==1.1.5',
        'easy-thumbnails==2.0.1',
        'feedparser==5.1.3',
        'google-api-python-client==1.3.1',
        'humanize==0.5',
        'jsonfield==1.0.0',
        'pyOpenSSL==0.14',
        'python-dateutil==2.2',
        'pytz==2012d',
        'requests==2.3.0',
        'singlemodeladmin==0.1',
        'twitter==1.14.3',
        # TODO package the following on our pypi
        # -e git://github.com/coleifer/micawber#egg=micawber
        # -e git://github.com/MotherNatureNetwork/django-suit@LOOP-330#egg=django-suit
    ],

    tests_require=[
        'coverage==3.7.1',
        'django-nose==1.2',
        'mock==1.0.1',
        'responses==0.3.0',
        'factory_boy==2.4.1',
    ],


    # List additional groups of dependencies here (e.g. development dependencies).
    # You can install these using the following syntax, for example:
    # $ pip install -e .[dev,test]
    extras_require = {
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    # package_data={
    #     'sample': ['package_data.dat'],
    # },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages.
    # see http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    # entry_points={
    #     'console_scripts': [
    #         'sample=sample:main',
    #     ],
    # },
)
