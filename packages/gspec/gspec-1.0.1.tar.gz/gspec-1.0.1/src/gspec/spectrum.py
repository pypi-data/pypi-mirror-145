from typing import DefaultDict
from collections import defaultdict
from typing import List
import numpy as np
import numpy.typing as npt
import os
from datetime import date


class gspectrum:

	energy_units: str
	count_time: float
	count_time_units: str
	meas_date: date
	spectrum_data: DefaultDict[int, float]

	def __init__(self) -> None:
		self.energy_units = 'keV'
		self.spectrum_data = defaultdict(float)

		self.count_time = 0.0
		self.count_time_units = 's'

		self.meas_date = date(1970, 1, 1)

	# Get the total number of counts in a specified window of the spectrum
	def get_counts(self, energies: List[int]) -> float:
		sum = 0.0
		for e in energies:
			sum += self.spectrum_data[e]
		return sum

	# Get the total count rate in a specified window of the spectrum
	# Units will be in counts per [count_time_units]
	def get_rate(self, energies: List[int]) -> float:
		return self.get_counts(energies) / self.count_time

	# Set the number of counts in a specified bin of the spectrum
	def set_counts(self, energy: int, counts: float) -> None:
		self.spectrum_data[energy] = counts

	# Add/subtract another spectrum from this one with optional scaling factor
	def add_spectrum(self, spec: 'gspectrum', factor: float = 1.0, force: bool = False) -> None:

		# Make sure spectra cannot be added with different count times unless forced
		count_time_ineq = (self.count_time != spec.count_time)
		count_time_unit_ineq = (self.count_time_units != spec.count_time_units)
		if not force and (count_time_ineq or count_time_unit_ineq):
			raise ValueError(
				f'Different count_time values ({self.count_time}{self.count_time_units} '
				f'vs {spec.count_time}{spec.count_time_units}). '
				f'Set force=True to ignore.'
			)

		for e, c in spec.spectrum_data.items():
			self.spectrum_data[e] += factor * c

	# Export spectrum as a text file
	# Exported spectrum will not contain gaps between integer energy values.
	# Missing values will be 0-filled.
	def print_txt(self, fp: str, force: bool = False) -> None:

		if not force and os.path.exists(fp):
			raise FileExistsError(f'File {fp} already exists. Set force=True to overwrite.')

		min_energy = min(self.spectrum_data.keys())
		max_energy = max(self.spectrum_data.keys())
		sz = max_energy - min_energy + 1
		data_array = np.zeros((sz, 2))
		for i in range(0, sz):
			data_array[i, 0] = min_energy + i
			data_array[i, 1] = self.spectrum_data[min_energy + i]

		np.savetxt(fp, data_array, fmt='%d\t%.5f', delimiter='\t', comments='',
			header=f'{self.count_time} {self.count_time_units} ({self.meas_date})\n'
						f'Energy [{self.energy_units}]\tCounts')


# Import spectrum from saved text file
def import_txt(fp: str) -> gspectrum:
	s = gspectrum()

	# Read spectrum part of file
	spec_data = np.loadtxt(fp, delimiter='\t', skiprows=2)
	for e, c in spec_data:
		s.spectrum_data[int(e)] = c

	# Read count time and units from the header
	with open(fp, 'r') as f:
		header1 = f.readline().rstrip().split()
		s.count_time = float(header1[0])
		s.count_time_units = header1[1]
		s.meas_date = date.fromisoformat(header1[2][1:11])
		header2 = f.readline().rstrip().split()
		s.energy_units = header2[1][1:-1]

	return s


# Import spectrum from numpy-array
def import_numpy(data: npt.NDArray[np.float_],
		count_time: float = 0.0, count_time_units: str = 's',
		energy_units: str = 'keV') -> gspectrum:
	s = gspectrum()
	s.count_time = count_time
	s.count_time_units = count_time_units
	s.energy_units = energy_units
	for e, c in data:
		s.set_counts(int(e), c)
	return s
