# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zodipy']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=5.0.1',
 'healpy>=1.15.0,<2.0.0',
 'jplephem>=2.17,<3.0',
 'numpy>=1.22.3,<2.0.0']

setup_kwargs = {
    'name': 'zodipy',
    'version': '0.5.1',
    'description': 'Zodipy is a python tool that simulates the Zodiacal emission.',
    'long_description': '\n<img src="imgs/zodipy_logo.png" width="350">\n\n[![PyPI version](https://badge.fury.io/py/zodipy.svg)](https://badge.fury.io/py/zodipy)\n![Tests](https://github.com/MetinSa/zodipy/actions/workflows/tests.yml/badge.svg)\n[![astropy](http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat)](http://www.astropy.org/)\n\n\n---\n\n\n*Zodipy* is a Python tool for simulating the Interplanetary Dust Emission that a Solar System observer sees, either in the form of timestreams or binned HEALPIX maps.\n\n![plot](imgs/zodipy_map.png)\n\n\n# Usage\nA full introduction to *Zodipy* and its use-cases can be found in the [documentation](https://zodipy.readthedocs.io/en/latest/).\n\n**Interplanetary Dust models:** select between built in models.\n```python\nfrom zodipy import Zodipy\n\nmodel = Zodipy(model="DIRBE") # DIRBE\nmodel = Zodipy(model="Planck18") # Planck 2018\n```\n\n**Get emission from a point on the sky:** choose a frequency/wavelength, an observer, a time of observation, and angular coordinates (co-latitude, longitude).\n```python\nimport astropy.units as u\nfrom astropy.time import Time\n\nmodel.get_emission(\n    25*u.micron,\n    obs="earth",\n    obs_time=Time.now(),\n    theta=10*u.deg,\n    phi=40*u.deg,\n)\n>> <Quantity [16.65684599] MJy / sr>\n```\n\n**Get emission from a sequence of angular coordinates:** `theta` and `phi` can be a sequence of angles that can represent some time-ordered pointing.\n```python\ntheta = [10.1, 10.5, 11.1, 11.5] * u.deg # Longitude\nphi = [40.2, 39.9, 39.8, 41.3] * u.deg # Latitude\n\nmodel.get_emission(\n    25*u.micron,\n    obs="earth",\n    obs_time=Time.now(),\n    theta=theta,\n    phi=phi,\n    lonlat=True,\n)\n>> <Quantity [29.11106315, 29.33735654, 29.41248579, 28.30858417] MJy / sr>\n```\n\n\n**Get emission from pixel indices on a HEALPIX grid:** a sequence of pixel indicies along with an NSIDE parameter can be used.\n```python\nmodel.get_emission(\n    25*u.micron,\n    obs="earth",\n    obs_time=Time.now(),\n    pixels=[24654, 12937, 26135],\n    nside=128,\n)\n>> <Quantity [17.77385144, 19.7889428 , 22.44797121] MJy / sr>\n```\n\n**Get binned emission component-wise:** the emission can be binned to a HEALPIX map, and also returned component-wise.\n```python\nimport healpy as hp\nimport numpy as np\n\nnside = 128\n\nmodel.get_emission(\n    25*u.micron,\n    obs="earth",\n    obs_time=Time.now(),\n    pixels=np.arange(hp.nside2npix(nside)),\n    nside=nside,\n    binned=True,\n    return_comps=True\n).shape\n>> (6, 196608)\n```\n\n# Documentation\nA detailed introduction along with a tutorial of how to use *Zodipy* will shortly be available in the [documentation](https://zodipy.readthedocs.io/en/latest/).\n# Installing\nZodipy is available on PyPI and can be installed with ``pip install zodipy`` (Python >= 3.8 required).\n\n# Scientific paper\n- San et al. (2022). *Zodipy: software for simulating Interplanetary Dust Emission.* Manuscript in preparation.\n\n\n<!-- *Zodipy* defaults to using the interplanetary dust model developed by the DIRBE team, and the `de432s` JPL ephemeris (10 MB file downloaded and cached first time `Zodipy` is initialized). The ephemeris is used to compute the position of the relevant Solar System bodies through the `astropy.coordinates.solar_system_ephemeris` api.  -->',
    'author': 'Metin San',
    'author_email': 'metinisan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MetinSa/zodipy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<=3.10',
}


setup(**setup_kwargs)
