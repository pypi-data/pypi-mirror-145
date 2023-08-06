# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['uval', 'uval.config', 'uval.stages', 'uval.tests', 'uval.utils']

package_data = \
{'': ['*'], 'uval': ['templates/*']}

install_requires = \
['Jinja2>=3.0.3,<4.0.0',
 'Pillow>=9.0.1,<10.0.0',
 'click>=8.0.4,<9.0.0',
 'fvcore>=0.1.5,<0.2.0',
 'h5py>=3.6.0,<4.0.0',
 'ipykernel>=6.9.2,<7.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'numpy>=1.22.3,<2.0.0',
 'pandas>=1.4.1,<2.0.0',
 'pipx>=1.0.0,<2.0.0',
 'randomname>=0.1.5,<0.2.0',
 'rich>=12.0.1,<13.0.0',
 'ruamel.yaml>=0.17.21,<0.18.0',
 'scikit-learn>=1.0.2,<2.0.0',
 'sphinx-rtd-theme>=1.0.0,<2.0.0',
 'tqdm>=4.63.0,<5.0.0']

entry_points = \
{'console_scripts': ['uval = uval.main:main']}

setup_kwargs = {
    'name': 'uval',
    'version': '0.1.7',
    'description': 'This python package is meant to provide a high level interface to facilitate the evaluation of object detection and segmentation algorithms that operate on 3D volumetric data.',
    'long_description': '&nbsp;![UVal](https://gitlab.com/smithsdetection/uval/-/raw/main/icon_uval.png) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[![Smiths Detection](https://gitlab.com/smithsdetection/uval/-/raw/main/SD_logo.png)](https://www.smithsdetection.com/ "Redirect to homepage")\n---\nUVal - Unified eValuation framework for 3D X-ray data\n---\n> This python package is meant to provide a high level interface to facilitate the evaluation of object detection and segmentation algorithms that operate on 3D volumetric data.\n---\n- There is a growing need for high performance detection algorithms using 3D data, and it is very important to be able to compare them. By far, there has not been a trivial solution for a straightforward comparison between different 3D detection algorithms.\n- This framework seeks a way to address the aforementioned problem by introducing a simple and standard layout of the popular HDF5 data format as input. \n- Each detection algorithm can export the results and groundtruth data according to the defined layout principles. Then, UVal can evaluate the performance and come up with common comparison metrics.\n\n| ![](3d_vol.gif "3d CT Volume") |  ![](https://gitlab.com/smithsdetection/uval/-/raw/main/dets_anim.gif "Detections") |\n| :---: | :---: |\n\n## Installation (non-development)\nIf you are not developing and only using UVal, you can simply install it as a `pypi` package; simply run:\n```shell\npip install uval\n```\n\nIf you would like to have UVal installation to be independant of a specific python environment, simply use `pipx` instead of `pip`.\n\nTo run the code you can type:\n```shell\nuval --config-file ${workspaceFolder}/output/example/config.yaml\n```\nFor an example of the outputs see [here](https://gitlab.com/smithsdetection/uval/-/tree/main/output/example) and the report [here](https://gitlab.com/smithsdetection/uval/-/raw/main/output/example/report.pdf).\n\nFor the details of each entry in the config file please see [here](https://gitlab.com/smithsdetection/uval/-/raw/main/src/uval/config/README.md).\n\n## Installation (development)\nWe recommend using the Anaconda package manager to create <em>virtual environment</em> for UVal:\n```shell\n# for Linux installation:\nwget https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh\nsh ./Anaconda3-2020.11-Linux-x86_64.sh\n```\n\n## Development setup\n\n* First, please clone the UVal\'s git repository by executing the following command:  \n  ```git clone https://gitlab.com/smithsdetection/uval.git```\n  \n\n* You will need a `python >= 3.8` environment to develop Uval.  \n  We recommend using Anaconda due to its ease of use:\n  ```shell\n  wget https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh\n  sh ./Anaconda3-2020.11-Linux-x86_64.sh\n  ```\n* Setting up a `conda virtual environment` with `python=3.8` using the following commands:\n  Install conda-lock with pip support.\n  ```shell\n  cd uval\n  conda-lock install --name UVALENV conda-lock.yml\n  poetry install\n  pre-commit install\n  ```\n  ALternatively, you can create your own conda environment from scratch. and follow with `poetry` and `pre-commit` installations.\n\n## Example code\n* A step-by-step walkthrough for reading and evaluating data with the UVal is available as a jupyter document:\n  * [jupyter notebook demo](https://gitlab.com/smithsdetection/uval/-/blob/main/demo/sample-data-evaluation.ipynb)\n------\n  * **Hint:** Prior to running the demo jupyter notebook walkthrough, the following steps must be performed:\n    \n    * The `ipykernel` conda package must be installed\n      ```shell\n      conda install -c anaconda ipykernel\n      ```\n    * The `uvalenv` environment must be added as an ipykernel: \n      ```shell  \n      python3 -m ipykernel install --user --name uvalenv --display-name "uvalenv Python38"\n      ```\n    * The `uvalenv Python38` kernel, which includes all the required python packages must be selected in `jupyter` environment to run the code.\n------\n\n## Documentations\nRead the docs: https://uval.readthedocs.io/\n\n## Release History\n\n* 0.1.x\n  * The first ready-to-use version of UVal releases publicly\n\n## Meta\n\nSmiths Detection – [@Twitter](https://twitter.com/smithsdetection) – uval@smithsdetection.com\n\n``UVal`` is released under the [GPL V3.0 license](LICENSE).\n\n## Contributing\n\n1. Fork it (<https://gitlab.com/smithsdetection/uval/fork>)\n2. Create your feature branch (`git checkout -b feature/fooBar`)\n3. Commit your changes (`git commit -am \'Add some fooBar\'`)\n4. Push to the branch (`git push origin feature/fooBar`)\n5. Create a new merge Request\n\n## Citing UVal\nIf you use UVal in your research or wish to refer to the results, please use the following BibTeX entry.\n\n```****BibTeX****\n@misc{smithsdetection2022uval,\n  author =       {Philipp Fischer, Geert Heilmann, Mohammad Razavi, Faraz Saeedan},\n  title =        {UVal},\n  howpublished = {\\url{https://gitlab.com/smithsdetection/uval}},\n  year =         {2022}\n}\n```',
    'author': 'Geert Heilmann',
    'author_email': 'geert.heilmann@smithsdetection.com',
    'maintainer': 'Faraz Saeedan',
    'maintainer_email': 'faraz.saeedan@smithsdetection.com',
    'url': 'https://gitlab.com/smithsdetection/uval',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
