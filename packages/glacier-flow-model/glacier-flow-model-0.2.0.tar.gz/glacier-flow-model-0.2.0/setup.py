# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['glacier_flow_model',
 'glacier_flow_model.data',
 'glacier_flow_model.fracd8',
 'glacier_flow_model.utils']

package_data = \
{'': ['*']}

install_requires = \
['GDAL>=3.4.1,<4.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'numba>=0.55.1,<0.56.0',
 'numpy>=1.19.0,<2.0.0',
 'scipy>=1.8.0,<2.0.0']

setup_kwargs = {
    'name': 'glacier-flow-model',
    'version': '0.2.0',
    'description': 'Modeling glaciers on a digital elevation model based on mass balance and a modified D8 flow algorithm applied to ice',
    'long_description': '.. image:: https://raw.githubusercontent.com/munterfi/glacier-flow-model/master/docs/source/_static/logo.svg\n   :width: 120 px\n   :alt: https://github.com/munterfi/glacier-flow-model\n   :align: right\n\n==================\nGlacier flow model\n==================\n\n.. image:: https://img.shields.io/pypi/v/glacier-flow-model.svg\n        :target: https://pypi.python.org/pypi/glacier-flow-model\n\n.. image:: https://github.com/munterfi/glacier-flow-model/workflows/check/badge.svg\n        :target: https://github.com/munterfi/glacier-flow-model/actions?query=workflow%3Acheck\n\n.. image:: https://readthedocs.org/projects/glacier-flow-model/badge/?version=latest\n        :target: https://glacier-flow-model.readthedocs.io/en/latest/\n        :alt: Documentation Status\n\n.. image:: https://codecov.io/gh/munterfi/glacier-flow-model/branch/master/graph/badge.svg\n        :target: https://codecov.io/gh/munterfi/glacier-flow-model\n\nModeling glaciers on a digital elevation model (DEM) based on mass balance and\na modified D8 flow algorithm applied to ice.\n\nThe modeling is based on a linear relationship between altitude and mass\nbalance, the so-called mass balance gradient. For alpine glaciers this gradient\nis about 0.006 m/m. Continental glaciers tend to be at 0.003 and maritime\nglaciers at 0.01 m/m. The alpine gradient is set by default in the model.\nTo model the glaciers, annual steps are calculated. First the mass balance\n(accumulation and ablation) for the area is added to the glacier layer and in a\nsecond step the glacier flow is simulated by using a modified D8 technique\n(submodule :code:`fracd8`).\nSince the prupose of the D8 flow direction algorithm is modeling surface water\nflows over terrain, the D8 algorithm was modified to be able to consider the\nfraction of ice that is flowing out of each cell based on the glaciers\nvelocity. In order to avoid pure convergence of the flow, the surface of the\nglaciers is slightly smoothed. The simulation stops when the observed\ndifference in mass balance for a smoothed curve (default\n:code:`MODEL_TREND_SIZE=100`) is less than a given tolerance (default\n:code:`MODEL_TOLERANCE=0.0001`).\n\nGetting started\n---------------\n\nThe **glacier-flow-model** package depends on GDAL, which needs to be installed\non the system.\n\nGet the stable release of the package from pypi:\n\n.. code-block:: shell\n\n    pip install glacier-flow-model\n\nExample data\n____________\n\nThe package includes an example DEM from `swisstopo <https://www.swisstopo.admin.ch/en/home.html>`_.\nIt covers a smaller extent around the Aletsch glacial arena in Switzerland with\na raster cell resolution of 200m.\n\n.. code-block:: python\n\n    from glacier_flow_model import PkgDataAccess\n    dem = PkgDataAccess.load_dem()\n\nThe original DEM can be downloaded `here <https://www.swisstopo.admin.ch/en/geodata/height/dhm25200.html>`_.\n\nUsage\n_____\n\nTo set up a glacier flow model, a path to a DEM in the GeoTiff file format has\nto passed to the model class constructor. By default the mass balance\nparameters for alpine glaciers in the year 2000 are set. Keep the input file\nsize small, otherwise the model may be slowed down remarkably:\n\n.. code-block:: python\n\n    import logging\n    from glacier_flow_model import GlacierFlowModel, PkgDataAccess\n\n    LOG_FORMAT = "[%(asctime)s %(levelname)s] %(message)s (%(name)s)"\n    logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)\n\n    gfm = GlacierFlowModel(PkgDataAccess.locate_dem())\n\nAfter initialization, the model needs to accumulate the initial ice mass until\nit reaches a steady state, call the :code:`reach_steady_state` method to do so:\n\n.. code-block:: python\n\n    gfm.reach_steady_state()\n\n.. image:: https://raw.githubusercontent.com/munterfi/glacier-flow-model/master/docs/source/_static/steady_state_initial.png\n   :alt: https://github.com/munterfi/glacier-flow-model\n   :align: center\n\nWhen the model is in a steady state, a temperature change of the climate can be\nsimulated. Simply use the :code:`simulate` method with a positive or negative\ntemperature change in degrees. The model changes the temperature gradually and\nsimulates years until it reaches a steady state again.\n\nHeating 4.5°C after initial steady state:\n\n.. code-block:: python\n\n    gfm.simulate(4.5)\n\n.. image:: https://raw.githubusercontent.com/munterfi/glacier-flow-model/master/docs/source/_static/steady_state_heating.png\n   :alt: https://github.com/munterfi/glacier-flow-model\n   :align: center\n\nCooling -3°C after initial steady state:\n\n.. code-block:: python\n\n    gfm.simulate(-3)\n\n.. image:: https://raw.githubusercontent.com/munterfi/glacier-flow-model/master/docs/source/_static/steady_state_cooling.png\n   :alt: https://github.com/munterfi/glacier-flow-model\n   :align: center\n\nExport the results of the model into :code:`.csv` and :code:`.tif` files:\n\n.. code-block:: python\n\n    gfm.export()\n\nThe GeoTiff contains the following bands, averaged over the last 10 simulation\nyears (default :code:`MODEL_RECORD_SIZE=10`):\n\n1. Glacier thickness [m].\n2. Velocity at medium height [m/a].\n3. Mass balance [m].\n\nCheck out the `video <https://munterfinger.ch/media/film/gfm.mp4>`_ of the scenario simulation in the Aletsch\nglacial arena in Switzerland\n\nLimitations\n-----------\n\nThe model has some limitations that need to be considered:\n\n- The flow velocity of the ice per year is limited by the resolution of the\n  grid cells. Therefore, a too high resolution should not be chosen for the\n  simulation.\n- The modeling of ice flow is done with D8, a technique for modeling surface\n  flow in hydrology. Water behaves fundamentally different from ice, which is\n  neglected by the model (e.g. influence of crevasses).\n- The flow velocity only considers internal ice deformation (creep). Basal\n  sliding, and soft bed deformation are ignored.\n- No distinction is made between snow and ice. The density of the snow or ice\n  mass is also neglected in the vertical column.\n\nLicense\n-------\n\nThis project is licensed under the MIT License - see the LICENSE file for\ndetails\n',
    'author': 'Merlin Unterfinger',
    'author_email': 'info@munterfinger.ch',
    'maintainer': 'Merlin Unterfinger',
    'maintainer_email': 'info@munterfinger.ch',
    'url': 'https://pypi.org/project/glacier-flow-model/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
