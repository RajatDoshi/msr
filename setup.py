from setuptools import setup
from setuptools import find_namespace_packages

setup(
  name='msr-by-rajat',
  version='1.0.1',
  description='Sym Backend Challenge',
  author='Rajat Doshi',
  author_email='rajat.doshi@yale.edu',
  packages=['msr'],
  install_requires=[
  "certifi==2020.12.5",
  "chardet==4.0.0",
  "decorator==4.4.2",
  "idna==2.10",
  "prettytable==2.0.0",
  "requests-futures==1.0.0",
  "requests==2.25.1",
  "semver==2.13.0",
  "six==1.15.0",
  "urllib3==1.26.2",
  "validators==0.18.2",
  "wcwidth==0.2.5",
  ],
  entry_points={
      'console_scripts': [
          'msr=msr.__main__:main'
      ]
  }
)