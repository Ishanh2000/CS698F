# Gesture Recognition

### CS698F: Sensing, Communication and Networking for Wireless Smart Devices, Fall 2021

Code for our course project on recognizing gestures with a handheld smartphone device's sensors.

## Dependencies 

The project has been written and tested with Python3.6 on an Linux system.

The following external packages are required, can be installed via `pip`:

```
numpy
matplotlib
tqdm (for progress bars)
scipy (preprocessing)
PyWavelets (wavelet denoising)
```

The scripts should be run from within the project directory, for example:

`python3 src/dtw_cosine.test.py`

## Repository Structure

- `raw_data`: Contains the raw sensor data collected for each gesture from the Physics Toolbox app. Each file contains about 10-15 executions of each gesture.
- `raw_templates`: Contains sensor data for each execution of the gestures, separated from the raw data. 
- `clean_templates`: Templates after preprocessing steps were applied (downsampling + filtering of choice)
- `src`: All the code scripts
- `plots`: Generated plots used in report and presentations.
- `times`: Execution time results for various algorithms
- `test`: Templates held out and used for testing.

## Scripts

- `split_data.py`: Used to separate the raw data CSVs into the raw gesture templates by manually specifying the sections for each gesture run.
- `plot.py`: Utilities to visualize the sensor data files.
- `preprocess.py`: Implements the preprocessing techniques - Downsampling, polynomial interpolation, low pass Butterworth filtering and wavelet denoising.
- `motif_match.py`: Attempt at generating matrix profile for the data. Requires `stumpy`. Please refer to the [Stumpy Documentation](https://stumpy.readthedocs.io/en/latest/index.html) for more details.
  
In general, each `name.test.py` file is a wrapper around the corresponding algorithm  `name`. 

- `DTW.py`: Basic DTW with Euclidean distance metric. Used for initial pipeline testing.
- `dtw_cosine.py`: Vanilla DTW with cosine similiarity weighted metric. Major improvements over Euclidean metric observed.
- `dtw_variants.py`: Implements DTW with the Sakoe Chiba band and the Itakura parallelogram. Constant order improvements in runtime.
- `fastdtw.py`: Implements FastDTW. Attempts were made to access the full path and cost matrix. Significant improvements in runtime.
- `dtw_online.py`: Takes in a long sensor data file and processes it in a windowed fashion. Emulating and observing behaviour in online settings.

## Script Parameters

When running the `.test.py` runners, please take note of the following defined variables (at the top of the file):

```
`TEST_FILE`: Path to the test sensor data file
`TEMPLATE_DIR`: Template directory to use (`clean_templates`/`raw_templates`)
`TIME_FILE`: File to store runtime data in
`NUM_RUNS`: Number of iterations to repeat the algorithm for (used to measure average runtime)
```

Within the `match_dtw_..` functions:

```
`gestures`: Which gestures to match the test data with
`num_templates`: Number of templates to average the matching over
```

## References

Soft DTW (quadratic) using CUDA cited from: [https://github.com/Maghoumi/pytorch-softdtw-cuda](https://github.com/Maghoumi/pytorch-softdtw-cuda)

FastDTW code slightly modified from: [https://github.com/slaypni/fastdtw](https://github.com/slaypni/fastdtw)

Other references mentioned in the attached report.