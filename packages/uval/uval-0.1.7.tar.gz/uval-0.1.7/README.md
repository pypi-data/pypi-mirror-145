&nbsp;![UVal](https://gitlab.com/smithsdetection/uval/-/raw/main/icon_uval.png) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[![Smiths Detection](https://gitlab.com/smithsdetection/uval/-/raw/main/SD_logo.png)](https://www.smithsdetection.com/ "Redirect to homepage")
---
UVal - Unified eValuation framework for 3D X-ray data
---
> This python package is meant to provide a high level interface to facilitate the evaluation of object detection and segmentation algorithms that operate on 3D volumetric data.
---
- There is a growing need for high performance detection algorithms using 3D data, and it is very important to be able to compare them. By far, there has not been a trivial solution for a straightforward comparison between different 3D detection algorithms.
- This framework seeks a way to address the aforementioned problem by introducing a simple and standard layout of the popular HDF5 data format as input. 
- Each detection algorithm can export the results and groundtruth data according to the defined layout principles. Then, UVal can evaluate the performance and come up with common comparison metrics.

| ![](3d_vol.gif "3d CT Volume") |  ![](https://gitlab.com/smithsdetection/uval/-/raw/main/dets_anim.gif "Detections") |
| :---: | :---: |

## Installation (non-development)
If you are not developing and only using UVal, you can simply install it as a `pypi` package; simply run:
```shell
pip install uval
```

If you would like to have UVal installation to be independant of a specific python environment, simply use `pipx` instead of `pip`.

To run the code you can type:
```shell
uval --config-file ${workspaceFolder}/output/example/config.yaml
```
For an example of the outputs see [here](https://gitlab.com/smithsdetection/uval/-/tree/main/output/example) and the report [here](https://gitlab.com/smithsdetection/uval/-/raw/main/output/example/report.pdf).

For the details of each entry in the config file please see [here](https://gitlab.com/smithsdetection/uval/-/raw/main/src/uval/config/README.md).

## Installation (development)
We recommend using the Anaconda package manager to create <em>virtual environment</em> for UVal:
```shell
# for Linux installation:
wget https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh
sh ./Anaconda3-2020.11-Linux-x86_64.sh
```

## Development setup

* First, please clone the UVal's git repository by executing the following command:  
  ```git clone https://gitlab.com/smithsdetection/uval.git```
  

* You will need a `python >= 3.8` environment to develop Uval.  
  We recommend using Anaconda due to its ease of use:
  ```shell
  wget https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh
  sh ./Anaconda3-2020.11-Linux-x86_64.sh
  ```
* Setting up a `conda virtual environment` with `python=3.8` using the following commands:
  Install conda-lock with pip support.
  ```shell
  cd uval
  conda-lock install --name UVALENV conda-lock.yml
  poetry install
  pre-commit install
  ```
  ALternatively, you can create your own conda environment from scratch. and follow with `poetry` and `pre-commit` installations.

## Example code
* A step-by-step walkthrough for reading and evaluating data with the UVal is available as a jupyter document:
  * [jupyter notebook demo](https://gitlab.com/smithsdetection/uval/-/blob/main/demo/sample-data-evaluation.ipynb)
------
  * **Hint:** Prior to running the demo jupyter notebook walkthrough, the following steps must be performed:
    
    * The `ipykernel` conda package must be installed
      ```shell
      conda install -c anaconda ipykernel
      ```
    * The `uvalenv` environment must be added as an ipykernel: 
      ```shell  
      python3 -m ipykernel install --user --name uvalenv --display-name "uvalenv Python38"
      ```
    * The `uvalenv Python38` kernel, which includes all the required python packages must be selected in `jupyter` environment to run the code.
------

## Documentations
Read the docs: https://uval.readthedocs.io/

## Release History

* 0.1.x
  * The first ready-to-use version of UVal releases publicly

## Meta

Smiths Detection – [@Twitter](https://twitter.com/smithsdetection) – uval@smithsdetection.com

``UVal`` is released under the [GPL V3.0 license](LICENSE).

## Contributing

1. Fork it (<https://gitlab.com/smithsdetection/uval/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new merge Request

## Citing UVal
If you use UVal in your research or wish to refer to the results, please use the following BibTeX entry.

```****BibTeX****
@misc{smithsdetection2022uval,
  author =       {Philipp Fischer, Geert Heilmann, Mohammad Razavi, Faraz Saeedan},
  title =        {UVal},
  howpublished = {\url{https://gitlab.com/smithsdetection/uval}},
  year =         {2022}
}
```