# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

setup(name='gribmagic',
      version='0.0.0',
      description='Download of public GRIB1/GRIB2 and netCDF data from numerical weather prediction models',
      long_description=README,
      license="AGPL 3, EUPL 1.2",
      classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Topic :: Communications",
        "Topic :: Database",
        "Topic :: Internet",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Archiving",
        "Topic :: Text Processing",
        "Topic :: Utilities",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS"
        ],
      author='Daniel Lassahn, Andreas Motl',
      author_email='andreas.motl@panodata.org',
      url='https://github.com/earthobservations/gribmagic',
      keywords='nwp weather data acquisition ' +
               'dwd icon cosmo ncep meteofrance arome knmi harmonie',
      packages=find_packages(),
      include_package_data=True,
      package_data={
        'gribmagic': [
          'unity/knowledge/*.yml',
        ],
      },
      zip_safe=False,
      test_suite='kotori.test',
      install_requires=[
        "requests>=2,<2.26",
        "cfgrib>=0.9,<1",
        "xarray>=0.16,<0.20",
        "cachetools>=4.2,<5",
        "PyYAML>=5.3,<5.5",
        "dask==2021.9.1",
        "click>=8,<9",
      ],
      extras_require={
        "test": [
          "pytest>=6,<7",
          "pytest-cov>=2.10,<3",
          "mock>=4,<5",
          "responses>=0.12,<1",
        ],
      },
      entry_points={
        'console_scripts': [
          'gribmagic = gribmagic.commands:cli',
        ],
      },
)
