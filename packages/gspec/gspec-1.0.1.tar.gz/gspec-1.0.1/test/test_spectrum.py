import unittest
import gspec
from pathlib import Path
import numpy as np
from datetime import date


class TestSpectrum(unittest.TestCase):

	def test_default_energy_units(self):
		s = gspec.gspectrum()
		self.assertEqual(s.energy_units, 'keV')

	def test_default_count_time(self):
		s = gspec.gspectrum()
		self.assertEqual(s.count_time, 0.0)
		self.assertEqual(s.count_time_units, 's')

	def test_default_meas_date(self):
		s = gspec.gspectrum()
		self.assertEqual(s.meas_date, date(1970, 1, 1))

	def test_default_data(self):
		s = gspec.gspectrum()
		self.assertEqual(len(s.spectrum_data), 0)

	def test_get_counts_no_data(self):
		s = gspec.gspectrum()
		self.assertEqual(s.get_counts([510, 511, 512]), 0)

	def test_set_counts(self):
		s = gspec.gspectrum()
		s.set_counts(509, 32.1)
		s.set_counts(510, 10.1)
		s.set_counts(511, 11.1)
		self.assertEqual(s.get_counts([510, 511, 512]), 21.2)

	def test_get_rate(self):
		s = gspec.gspectrum()
		s.set_counts(509, 9.0)
		s.set_counts(510, 10.0)
		s.set_counts(511, 11.0)
		s.count_time = 10.0
		self.assertEqual(s.get_rate([509, 510, 511]), 3.0)

	def test_addition(self):
		s1 = gspec.gspectrum()
		s1.set_counts(509, 32.1)
		s1.set_counts(510, 10.1)
		s1.set_counts(511, 11.1)

		s2 = gspec.gspectrum()
		s2.set_counts(508, 1.0)
		s2.set_counts(509, 1.1)
		s2.set_counts(510, 1.2)

		s1.add_spectrum(s2)
		self.assertEqual(s1.get_counts([508]), 1.0)
		self.assertEqual(s1.get_counts([509]), 33.2)
		self.assertAlmostEqual(s1.get_counts([510]), 11.3)
		self.assertEqual(s1.get_counts([511]), 11.1)
		self.assertEqual(s1.get_counts([512]), 0.0)

		self.assertEqual(s2.get_counts([508]), 1.0)
		self.assertEqual(s2.get_counts([509]), 1.1)
		self.assertEqual(s2.get_counts([510]), 1.2)
		self.assertEqual(s2.get_counts([511]), 0.0)

	def test_addition_error_wrong_count_time(self):
		s1 = gspec.gspectrum()
		s1.set_counts(509, 32.1)
		s1.set_counts(510, 10.1)
		s1.set_counts(511, 11.1)
		s1.count_time = 1.0

		s2 = gspec.gspectrum()
		s2.set_counts(508, 1.0)
		s2.set_counts(509, 1.1)
		s2.set_counts(510, 1.2)

		self.assertRaises(ValueError, s1.add_spectrum, s2)
		try:
			s1.add_spectrum(s2)  # Should throw exception
			self.fail()  # Should not reach this point
		except ValueError as e:
			self.assertEqual(str(e),
				'Different count_time values (1.0s vs 0.0s). '
				'Set force=True to ignore.')

	def test_addition_error_wrong_count_time_units(self):
		s1 = gspec.gspectrum()
		s1.set_counts(509, 32.1)
		s1.set_counts(510, 10.1)
		s1.set_counts(511, 11.1)
		s1.count_time = 1.0
		s1.count_time_units = 'm'

		s2 = gspec.gspectrum()
		s2.set_counts(508, 1.0)
		s2.set_counts(509, 1.1)
		s2.set_counts(510, 1.2)
		s2.count_time = 1.0
		s2.count_time_units = 'h'

		self.assertRaises(ValueError, s1.add_spectrum, s2)
		try:
			s1.add_spectrum(s2)  # Should throw exception
			self.fail()  # Should not reach this point
		except ValueError as e:
			self.assertEqual(str(e),
				'Different count_time values (1.0m vs 1.0h). '
				'Set force=True to ignore.')

	def test_addition_force_wrong_count_time(self):
		s1 = gspec.gspectrum()
		s1.set_counts(509, 32.1)
		s1.set_counts(510, 10.1)
		s1.set_counts(511, 11.1)
		s1.count_time = 1.0

		s2 = gspec.gspectrum()
		s2.set_counts(508, 1.0)
		s2.set_counts(509, 1.1)
		s2.set_counts(510, 1.2)

		s1.add_spectrum(s2, force=True)
		self.assertEqual(s1.get_counts([509]), 33.2)

	def test_subtraction(self):
		s1 = gspec.gspectrum()
		s1.set_counts(509, 32.1)
		s1.set_counts(510, 10.1)
		s1.set_counts(511, 11.1)

		s2 = gspec.gspectrum()
		s2.set_counts(508, 1.0)
		s2.set_counts(509, 1.1)
		s2.set_counts(510, 1.2)

		s1.add_spectrum(s2, factor=-1.0)
		self.assertEqual(s1.get_counts([508]), -1.0)
		self.assertEqual(s1.get_counts([509]), 31.0)
		self.assertEqual(s1.get_counts([510]), 8.9)
		self.assertEqual(s1.get_counts([511]), 11.1)
		self.assertEqual(s1.get_counts([512]), 0.0)

		self.assertEqual(s2.get_counts([508]), 1.0)
		self.assertEqual(s2.get_counts([509]), 1.1)
		self.assertEqual(s2.get_counts([510]), 1.2)
		self.assertEqual(s2.get_counts([511]), 0.0)

	def test_print_txt(self):
		# Remove existing file
		Path('test/spec_a3h7.txt').unlink(missing_ok=True)
		s = gspec.gspectrum()
		s.count_time = 15000.0
		s.count_time_units = 'ms'
		s.energy_units = 'eV'
		s.meas_date = date(2000, 12, 13)
		s.set_counts(34, 1.4)
		s.set_counts(35, 2.0)
		s.set_counts(37, 0.2)
		s.print_txt('test/spec_a3h7.txt')
		with open('test/spec_a3h7.txt', 'r') as f:
			self.assertEqual(f.readline(), '15000.0 ms (2000-12-13)\n')
			self.assertEqual(f.readline(), 'Energy [eV]\tCounts\n')
			self.assertEqual(f.readline(), '34\t1.40000\n')
			self.assertEqual(f.readline(), '35\t2.00000\n')
			self.assertEqual(f.readline(), '36\t0.00000\n')
			self.assertEqual(f.readline(), '37\t0.20000\n')
			self.assertEqual(f.readline(), '')

	def test_print_no_overwrite(self):
		with open('test/spec_a3h7.txt', 'w') as f:
			f.write('TESTESTEST\n')

		s = gspec.gspectrum()
		s.count_time = 15000.0
		s.count_time_units = 'ms'
		s.energy_units = 'eV'
		s.set_counts(34, 1.4)
		s.set_counts(35, 2.0)
		s.set_counts(37, 0.2)
		self.assertRaises(FileExistsError, s.print_txt, 'test/spec_a3h7.txt')
		try:
			s.print_txt('test/spec_a3h7.txt')  # Should throw exception
			self.fail()  # Should never reach here
		except FileExistsError as e:
			self.assertEqual(str(e),
				'File test/spec_a3h7.txt already exists. Set force=True to overwrite.')

		with open('test/spec_a3h7.txt', 'r') as f:
			self.assertEqual(f.readline(), 'TESTESTEST\n')
			self.assertEqual(f.readline(), '')

	def test_print_force_overwrite(self):
		with open('test/spec_a3h7.txt', 'w') as f:
			f.write('TESTESTEST\n')

		s = gspec.gspectrum()
		s.count_time = 15000.0
		s.count_time_units = 'ms'
		s.energy_units = 'eV'
		s.set_counts(34, 1.4)
		s.set_counts(35, 2.0)
		s.set_counts(37, 0.2)
		s.print_txt('test/spec_a3h7.txt', force=True)
		with open('test/spec_a3h7.txt', 'r') as f:
			self.assertEqual(f.readline(), '15000.0 ms (1970-01-01)\n')
			self.assertEqual(f.readline(), 'Energy [eV]\tCounts\n')
			self.assertEqual(f.readline(), '34\t1.40000\n')
			self.assertEqual(f.readline(), '35\t2.00000\n')
			self.assertEqual(f.readline(), '36\t0.00000\n')
			self.assertEqual(f.readline(), '37\t0.20000\n')
			self.assertEqual(f.readline(), '')


class TestImport(unittest.TestCase):

	def test_import_txt(self):
		s = gspec.import_txt('test/spec_a2h6.txt')

		self.assertEqual(s.count_time, 300.0)
		self.assertEqual(s.count_time_units, 'm')
		self.assertEqual(s.energy_units, 'MeV')
		self.assertEqual(s.meas_date, date(2021, 11, 30))

		# Check types of data in the array
		x = s.spectrum_data
		y = min(x)
		yy = x[y]
		self.assertIsInstance(y, int)
		self.assertIsInstance(yy, float)

		self.assertEqual(len(s.spectrum_data), 600)
		self.assertEqual(s.get_counts([23]), 0.0)
		self.assertEqual(s.get_counts([63]), 601.89345)
		self.assertEqual(s.get_counts([371]), 53.05888)
		self.assertEqual(s.get_counts([600]), 0.0)

	def test_import_numpy(self):
		s = gspec.import_numpy(np.array([[10, 231.0], [11, 232.2], [12, 0.0], [13, 2.0]]))

		self.assertEqual(s.count_time, 0.0)
		self.assertEqual(s.count_time_units, 's')
		self.assertEqual(s.energy_units, 'keV')
		self.assertEqual(len(s.spectrum_data), 4)

		x = s.spectrum_data
		y = min(x)
		yy = x[y]
		self.assertIsInstance(y, int)
		self.assertIsInstance(yy, float)

		self.assertEqual(s.get_counts([10]), 231.0)
		self.assertEqual(s.get_counts([11]), 232.2)
		self.assertEqual(s.get_counts([12]), 0.0)
		self.assertEqual(s.get_counts([13]), 2.0)

	def test_import_numpy_units(self):
		s = gspec.import_numpy(np.array([[10, 231.0], [11, 232.2], [12, 0.0], [13, 2.0]]),
			count_time=30.2, count_time_units='m', energy_units='eV')

		self.assertEqual(s.count_time, 30.2)
		self.assertEqual(s.count_time_units, 'm')
		self.assertEqual(s.energy_units, 'eV')
		self.assertEqual(len(s.spectrum_data), 4)
		self.assertEqual(s.get_counts([10]), 231.0)
		self.assertEqual(s.get_counts([11]), 232.2)
		self.assertEqual(s.get_counts([12]), 0.0)
		self.assertEqual(s.get_counts([13]), 2.0)
