import unittest
import gspec
import datetime


class TestMediso(unittest.TestCase):

	def test_meas_time(self):
		s = gspec.read_mediso('test/00000001.dcm')
		self.assertEqual(s.count_time, 300)
		self.assertEqual(s.count_time_units, 's')

	def test_energy_units(self):
		s = gspec.read_mediso('test/00000001.dcm')
		self.assertEqual(s.energy_units, 'keV')

	def test_date(self):
		s = gspec.read_mediso('test/00000001.dcm')
		self.assertEqual(s.meas_date, datetime.date(2021, 10, 13))

	def test_spec_data(self):
		s = gspec.read_mediso('test/00000001.dcm')
		self.assertEqual(s.get_rate([0]), 0.0)
		self.assertEqual(s.get_counts([0]), 0.0)
		self.assertEqual(s.get_rate([24]), 0.0)
		self.assertEqual(s.get_counts([24]), 0.0)
		self.assertEqual(s.get_rate([25]), 0.047816)
		self.assertEqual(s.get_counts([25]), 14.3448)
		self.assertEqual(s.get_rate([172]), 16.815001)
		self.assertEqual(s.get_counts([172]), 5044.5003)
		self.assertEqual(s.get_rate([597]), 0.235407)
		self.assertEqual(s.get_counts([597]), 70.6221)
		self.assertEqual(s.get_rate([598]), 0.0)
		self.assertEqual(s.get_counts([598]), 0.0)
