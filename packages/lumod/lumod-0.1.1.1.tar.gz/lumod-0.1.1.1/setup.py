# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lumod', 'lumod.fluxes', 'lumod.models', 'lumod.tools']

package_data = \
{'': ['*'], 'lumod': ['data/*']}

install_requires = \
['matplotlib', 'numba', 'numpy', 'pandas']

setup_kwargs = {
    'name': 'lumod',
    'version': '0.1.1.1',
    'description': 'Hydrological Lumped Model Tools',
    'long_description': '# **Lumped Models (LuMod) for Hydrology**\n\n**LuMod** is an easy to use set of Lumped Models for hydrological simulation in Python language.\n\nCompared with other source codes that pretend to be fast, **LuMod** was created to facilitate the modeling and the results processing. Moreover, some features of **LuMod** are compiled with [numba](http://numba.pydata.org/) to increase simulation speed.\n\n\n## **Documentation**\n\nFull documentation and examples are available here: [LuMod-Docs](https://zaul_ae.gitlab.io/lumod-docs)\n\nInstallation is available from PyPI: [LuMod project](https://pypi.org/project/lumod/)\n\n## **Key Features**\n\n**LuMod** incorporates well know hydrological models with different structures:\n\n* **MILC**: One layer Lumped version of the MISDc model adapted for continous daily simulation.\n* **HYMOD**: Rainfall-Runoff Model based on the Probability-Distributed Model concept that runs at daily timestep.\n* **HBV**: Modified version of the Hydrologiska Byråns Vattenbalansavdelning (HBV) model.\n* **GR4J**: Well known daily rain-runoff model that depends of four parameters.\n* **GR2M**: Monthly rain-runoff model that depends of two parameters.\n* **GR1A**: One parameter annual rain-runoff model.\n* **MonteCarlo**: Random-based simulation for parameters optimization and uncertainty analysis.\n\n## **Quick installation**\n\nThe easier way to install **LuMod** is using [PyPI](https://pypi.org/):\n\n```bash\npip install lumod\n```\n\n## **Basic Example**\n\n**LuMod** was thought to be easy to use and compatible with libraries dedicated to DataScience, so it works with Pandas and Matplotlib to facilitate the analysis of simulations.\n\n```python\n# Import modules\nimport pandas as pd\nimport matplotlib.pyplot as plt\nimport lumod\nfrom lumod import tools\n\n# Load example data\ninfo, forcings = lumod.load_example(2)\n\n# Create a model\nmodel = lumod.models.GR4J(area=info.area, lat=info.lat)\nprint(model)\n\n# Run your model\nsimulations = model.run(forcings)\n\n# Validate your model\ntools.plots.model_evaluation(forcings.prec, forcings.qt, simulations.qt)\n```\n\n## **Citation**\n\n*Coming Soon*\n\n## **Author**\n\n**Main Developer**\n\nSaúl Arciniega Esparza, Ph.D., Full Time Associate Professor at the [Faculty of Engineering](https://www.ingenieria.unam.mx/) at the [National Autonomous University of Mexico](https://www.unam.mx/), working on the [Hydrogeology Group](https://www.ingenieria.unam.mx/hydrogeology/).\n\n[LinkedIn](https://www.linkedin.com/in/saularciniegaesparza/) | [Twitter](https://twitter.com/zaul_arciniega) | [ResearchGate](https://www.researchgate.net/profile/Saul-Arciniega-Esparza)\n\n',
    'author': 'Saul Arciniega Esparza',
    'author_email': 'zaul_ae@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/Zaul_AE/lumod',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
