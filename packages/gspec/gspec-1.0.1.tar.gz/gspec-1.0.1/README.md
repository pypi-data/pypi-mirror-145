# gspec
Python tool for working with gamma spectroscopy data

![Tests](https://github.com/cwand/gspec/actions/workflows/tests.yml/badge.svg)

## Installation
gpsc is most easily installed with pip:
```text
pip install gspec
```

## Usage
The central class in the gspec package is the `gspectrum` class:

```text
import gspec

spec = gspec.gspectrum()
```

### Variables
The `gspectrum` object will contain a few variables, that can be changed at will:

```text
from datetime import date

spec.energy_units = 'eV'            # Default: 'keV'
spec.count_time = 30.0              # Default: 0.0
spec.count_time_units = 'min'       # Default: 's'
spec.meas_date = date(2021,11,20)   # Default: date(1970,1,1)
```
These variables are used when plotting a spectrum or when adding and subtracting spectra.

### Adding data
One can add data to a `gspectrum` object manually
```text
spec.set_counts(152, 673.1) # Sets the number of counts at 152eV to 673.1
```
One can also create a spectrum object with pre-loaded data in a numpy-array:
```text
import numpy as np

n = np.array([[10, 231.0], [11, 232.2], [12, 0.0], [13, 2.0]])
spec = gspec.import_numpy(n)
```

### Getting data
To get the total counts, or the total count-rate, in a certain energy window of the spectrum:
```text
total_counts = spec.get_counts([32,33,78])    # Gets the sum of counts in the three bins (not necessarily continuous)
total_rate = spec.get_rate(range(45,50))      # Gets the total count rate  in the window between 45eV and 49eV (inclusive).
```
The count rate is simply computed as the total counts divided by the count_time variable.

### Adding and subtracting spectra
Spectra can be added (e.g. in case of multiple detectors) or subtracted (e.g. in case of background subtraction)
```text
bkg = np.array([[10, 13.0], [11, 13.1]]])
spec2 = gspec.import_numpy(bkg, count_time=30.0, count_time_units='min', energy_units='eV')
spec2.meas_date = date(2021,11,20) 
spec.add_spectrum(spec2, factor=-1.0, force=False)   # force=False is default and can be ignored here
```
This will subtract `spec2` from `spec` (in place). The `spec2` object will be unchanged. The `factor=-1.0` changes the addition to subtraction and can be any real number.
If the count times or time units are not equal, one will have to set `force=True` to enforce the addition.

### Saving and loading spectra
The spectrum can be saved in a text file:
```text
spec.print_txt('spectrum.txt', force=False)  # Set force=True to overwrite exisiting files with the same name
```

To load the spectrum later:
```text
spec3 = gspec.import_txt('spectrum.txt')
```

### Plotting
The spectrum can be plotted in a figure (this will block execution of the program)
```text
gspec.plot(spec, spectrum_string="Some title", windows=[[20, 22], [30, 35]], bkg=spec2, bkg_string="Some background", title="Figure title")
```
All input arguments after the first one are optional.
