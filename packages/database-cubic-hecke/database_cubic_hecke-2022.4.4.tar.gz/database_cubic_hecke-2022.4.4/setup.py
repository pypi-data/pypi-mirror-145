from setuptools import setup

package_name = 'database_cubic_hecke'

def local_scheme(version):
    return ""

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name=package_name,
  packages=[package_name],
  package_dir={package_name: package_name},
  license='GPL',
  description='Ivan Marin\'s representations of the cubic Hecke algebra on 4 strands as Python dictionaries',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author='Sebastian Oehms',
  author_email='seb.oehms@gmail.com',
  url='https://github.com/soehms/database_cubic_hecke',
  keywords=['Hecke', 'algebra', 'SageMath', 'database', 'cyclotomic', 'Markov', 'mathematics' ],
  install_requires=[],
  classifiers=[  # Optional
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 4 - Beta',
    # Whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3'
  ],
  use_scm_version={"local_scheme": local_scheme},
  setup_requires=['setuptools_scm'],
)
