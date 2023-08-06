# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simsi_transfer', 'simsi_transfer.utils']

package_data = \
{'': ['*'],
 'simsi_transfer.utils': ['ThermoRawFileParser/*',
                          'maracluster/linux64/*',
                          'maracluster/win64/*']}

install_requires = \
['lxml>=4.8.0,<5.0.0',
 'numpy>=1.18.1,<2.0.0',
 'pandas>=1.3.0,<2.0.0',
 'pyteomics>=4.5.3,<5.0.0']

setup_kwargs = {
    'name': 'simsi-transfer',
    'version': '0.2.0',
    'description': 'Software-assisted reduction of missing values in phosphoproteomics and proteomics isobaric labeling data using MS2 spectrum clustering',
    'long_description': '# SIMSI-Transfer\n\nTool for increasing PSM gain from MaxQuant output file. Requires "Experiment" set in MaxQuant! \n\nFor testing SIMSI-Transfer after installation, we recommend downloading the TMT11 MS2 raw files from this publication:  \nThompson, A., Wölmer, N., Koncarevic, S., Selzer, S. et al., _TMTpro: Design, Synthesis, and Initial Evaluation of a Proline-Based Isobaric 16-Plex Tandem Mass Tag Reagent Set._ Analytical Chemistry 2019, 91, 15941–15950. doi:10.1021/acs.analchem.9b04474\n\nThe MaxQuant and SIMSI-Transfer results of the processed dataset can be downloaded from the following DOIs:  \n- MaxQuant output (required as input for SIMSI-Transfer): 10.5281/zenodo.6365902\n- SIMSI-Transfer output: 10.5281/zenodo.6365638\n\n## Running SIMSI-Transfer using the GUI\n\nOn Windows, you can download the `SIMSI-Transfer_GUI_windows.zip` from the latest release, unzip it and open `SIMSI-Transfer.exe` to start the GUI (no installation necessary).\n\nAlternatively, on all platforms, first install SIMSI-Transfer as explained below. Then install `PyQt5` (`pip install PyQt5`) and run:\n\n```shell\npython gui.py\n```\n\n## Running SIMSI-Transfer from the command line\n\nFirst install SIMSI-Transfer as explained below, then run SIMSI-Tranfer:\n\n```shell\npython -m simsi_transfer --mq_txt_folder </path/to/txt/folder> --raw_folder </path/to/raw/folder> --output_folder </path/to/output/folder>\n```\n\n## Installation\n\nSIMSI-Tranfer is available on PyPI and can be installed with `pip`:\n\n```shell\npip install simsi-transfer\n```\n\nAlternatively, you can install directly from this repository:\n\n```shell\ngit clone https://github.com/kusterlab/SIMSI-Transfer.git\npip install .\n```\n\n## Building the GUI on Windows\n\n### Create a conda environment\n\nTry importing `conda_environment.yml` in the Anaconda environment tab.\n\nIf that does not work, try the following:\n\n1. Set up a new environment, either through the Anaconda UI, or by running the following on the command line:\n\n```\nconda create -n simsi_transfer_gui python=3.8\nactivate simsi_transfer_gui\n```\n\n2. There are some caveats with installing the dependencies. We want to avoid dependence on the MKL (Math Kernel Library) package by numpy/scipy, as this blows up the size of the .exe file over 200MB (see [here](https://github.com/pyinstaller/pyinstaller/issues/2270)).\n\n```\nconda install -c conda-forge nomkl numpy pandas pyqt pyinstaller\nconda install -c bioconda pyteomics\n```\n\n### Building a self-contained executable\n\nUse the `build_gui.bat` script to create a self-contained executable.\n\n\n### Reducing size of the executable\n\nDownload UPX (https://upx.github.io/) to reduce the DLL file sizes, change the path in `build_gui.bat` to point to the UPX **folder**.\n',
    'author': 'Firas Hamood',
    'author_email': 'firas.hamood@tum.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kusterlab/SIMSI-Transfer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
