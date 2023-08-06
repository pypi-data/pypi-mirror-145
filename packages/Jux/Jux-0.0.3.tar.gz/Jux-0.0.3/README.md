# Jux : Solar X-Ray Burst Detector

<!-- <img align="right" style="padding-left: 20px" width="190" height="190" src="./assets/logo.jpg"> -->

<!-- This package was created by Team 10 on the account of Inter IIT Techmeet 10. -->
This package is concerned with identification and analysis of solar xray bursts in provided light curves. This package enables the user to analyse a lightcurve file through a multi-filter based approach resulting in a less noisy data and important flare paramters that can be fed to a Machine Learning Model for the detection of outliers among the flares in the given lightcurve.

## How to install it?  

```bash
pip install jux
```

Dependencies will build and you can proceed using it.

## How to use it?

Inorder to use this package on a specific lightcurve file import the Lightcurve class from jux.jux. Create an instance of the Lightcurve class passing the path to the LightCurve file as an argument. The Lightcurve class contains mainly two functions: 

- **Lightcurve.main()**
  - The parameters to the function are:

    1. *picklePath* - The path to an existing Pickle file containing the model parameters.
    
    2. *check_false_positives* - This argument is set to **False** by default so the function returns  the dataframe constructed with important parameters obtained from the filtered lightcurve data. Then this dataframe can be passed as an argument to the **Lightcurve.train_classifier()** method which will internally train a RandomForest model and save the model in a pickle file in the working directory. the output of the *train_classifier* method is the dataframe with outlier labels and corresoponds outlier scores. If this is set to **True**, the functions expects the pickle path of the model for inference,

- **Lightcurve.train_classifier()**
  - The parameters to the function are: 
    
    1. *model_zip* - the dataframe containing parameters like "_id", "time_ratio", "intensity_ratio", "bandwidth_1", "bandwidth_2", "error", which is obtained after passing the file to the **main** function.

## Demo 
```python
from jux.jux import Lightcurve
lc = Lightcurve(path_to_lc_file)
X = lc.main(check_false_positives=False)
Y = lc.train_classifier(x)
```

These are the followng submodules present in this package:

- `helper.py` : Contains helper functions including analytical functions that were fitted to the posterior part of a flare.
- `denoise.py` : Contains 3 algorithms including smoothening with fft, smoothening with median windowing and moving average smoothening.
- `flare_detect_minmax.py` : Contains 7 deterministic and condition based filters that help pick out bursts from de-noised data.
- `jux.py` : The main file containing class `Lightcurve` that accepts file path as argument, The main function will execute all de-noising and filtering and give out flare details and model fitted parameters that can then be used in the Isolation Classifier to detect false positives.
- `false_positive_detection.py` : Contains the functions that can be uses sklearn's Isolation Classifier to pick out outliers in the flares detected by the algorithm implemented above.
- `params.py` : Contains parameters that control all of the algorithms, context mentioned in the file itself.
- `create_df_minmax.py` : Contains functions that handles the dataframe given as the output by filtering.

## Algorithms explained

### Smoothening of LC

Lightcurve we trained upon has quite a bit of noise, so for de-noising we tried the following:

- Moving Averaging : Taking a small window and taking its mean as the corresponding value for the whole interval, thus effectively reducing the time scale thus this is followed by interpolation
- Interpolation :
  - Linear : We opted for Linear Interpolation because of its faster time complexity and not much effect in the results to our filtering algorithms
  - Spline : Spline interpolation was tried and performed the best with the filters, but took much longer time, with complexity O(m^2\*n)
- FFT Smoothing : Taking the FFT of the whole Light Curve wouldn't be possible as the signal is discontinuous, because we are only considering the GTI (Good Time Intervals). Thus doing that for every interval and again linear interpolation was done.

### Filters used

- Filter 0 : Minima and Maxima detected
- Filter 1 : Pairing of minima and maxima
- Filter 2 : Slope Thresholding implemented
- Filter 3 : Height Thresholding implemented
- Filter 4 : Repeated pairs filtered off
- Filter 5 : Close flares filtered off

These filters together actually gave a great result in picking out what we perceived as flares, sharp rises and slow decays.



