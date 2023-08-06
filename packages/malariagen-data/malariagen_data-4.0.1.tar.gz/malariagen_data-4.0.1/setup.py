# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['malariagen_data']

package_data = \
{'': ['*']}

install_requires = \
['BioPython',
 'bokeh',
 'dask[array]',
 'fsspec',
 'gcsfs',
 'importlib_metadata',
 'ipinfo',
 'ipyleaflet',
 'ipywidgets',
 'numba',
 'numpy',
 'plotly',
 'scikit-allel',
 'scipy',
 'statsmodels',
 'xarray',
 'zarr']

extras_require = \
{':python_version > "3.7" and python_version < "3.10"': ['pandas'],
 ':python_version >= "3.7" and python_version < "3.8"': ['pandas<1.4.0']}

setup_kwargs = {
    'name': 'malariagen-data',
    'version': '4.0.1',
    'description': 'A package for accessing and analysing MalariaGEN data.',
    'long_description': None,
    'author': 'Alistair Miles',
    'author_email': 'alistair.miles@sanger.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
