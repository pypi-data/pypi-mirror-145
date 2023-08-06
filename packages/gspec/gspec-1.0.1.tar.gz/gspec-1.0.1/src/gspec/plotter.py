from .spectrum import gspectrum
import matplotlib.pyplot as plt
import numpy as np
from typing import List
from typing import Tuple
from typing import Optional


def plot(
	spectrum: gspectrum, spectrum_string: str = "Spectrum",
	windows: List[Tuple[int, int]] = [],
	bkg: Optional[gspectrum] = None, bkg_string: str = "Background",
	title: str = "Spectrum") -> None:

	# Convert spectrum data to numpy data
	min_energy = min(spectrum.spectrum_data.keys())
	max_energy = max(spectrum.spectrum_data.keys())
	sz = max_energy - min_energy + 1
	data_array = np.zeros((sz, 2))
	for i in range(0, sz):
		data_array[i, 0] = min_energy + i
		data_array[i, 1] = spectrum.get_counts([min_energy + i])

	plt.plot(data_array[:, 0], np.zeros_like(data_array[:, 0]), color='k')
	plt.plot(data_array[:, 0], data_array[:, 1], label=spectrum_string)

	for window in windows:
		xlist = np.arange(window[0], window[1] + 1, 1.0)
		ylist = data_array[window[0]:window[1] + 1, 1]
		plt.fill_between(xlist, ylist)

	if bkg is not None:
		# Convert background data to numpy data
		bkg_min_energy = min(bkg.spectrum_data.keys())
		bkg_max_energy = max(bkg.spectrum_data.keys())
		bkg_sz = bkg_max_energy - bkg_min_energy + 1
		bkg_array = np.zeros((bkg_sz, 2))
		for i in range(0, bkg_sz):
			bkg_array[i, 0] = bkg_min_energy + i
			bkg_array[i, 1] = bkg.get_counts([bkg_min_energy + i])
		plt.plot(bkg_array[:, 0], bkg_array[:, 1],
			linestyle='--', color='0.4', label=bkg_string)

	plt.legend()
	plt.xlabel("Energy [{}]".format(spectrum.energy_units))
	plt.ylabel("Counts")
	plt.title(title)
	plt.show()
