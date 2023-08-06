# Use Uval Configurations

Uval code runs need a config file that includes a subset of the following fields. The missing fields will be replaced by the default values.

## ENV

* CACHE_FOLDER: The folder to cache the data. Default:uval_root

## DATA

* PATH: Where to find the dataset. Default:uval_root/data/hdf5.
* IGNORE_MISSING_FILES: When True, files from the YAML that do not exist in data folder are ignored. Default:False
* MAX_THREADS: The number of loaders to load .h5 files. Default:8.
  
## DATA_SPLIT

* YAML: The YAML file containing the split information. Default:uval_root/data/datasplit/uval_ds.yaml
* SUBSET: Which subset of the data to run the test on. Default: ["train", "test"]
  
## METRICS

* FACTOR: Factor for F-score. Default:1
* IOU_THRESHOLD: IOU threshold For single IOU evaluations. Otherwise ignored. Default:0.3
* IOU_RANGE: The range of IOUs for evaluation. Ignored when set to anything other than a tuple. Default:(0,)
* MAX_PROCESSES: Number of processes used to calculate range IOU recalls. Default:4.
* CONFIDENCE_THRESHOLD: Confidence threshold For single Confidence evaluations. Otherwise ignored. Default:0.6
* AP_METHOD = choose between VOC2007 and VOC2012 type evaluation. Default: "EveryPointInterpolation" (VOC2012)

## OUTPUT

* PATH: Where to store the output. Default: a new folder named after the current time.
* TEMPLATES_PATH = Where to load report html templates. Default: /uval_root/src/uval/templates
* CONFIG_FILE = Default: "config.yaml"
* REPORT_FILE = Output report file name. Default:report.html
* METRICS_FILE = File to save the serialized version of the calculated metrics. Default:metrics.pickle
* DATASET_OVERVIEW_FILE = Detailed information about the dataset. Default:dataset_overview.csv
