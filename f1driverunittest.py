__author__ = 'Shiven'

import f1drivers
import unittest


class TestURLBuilder(unittest.TestCase):

    def test_url_drivstand_data_type(self):
        self.assertEqual(f1drivers.build_url(2010, "driverStandings"), "http://ergast.com/api/f1/2010/driverStandings.json")

    def test_url_drivers_data_type(self):
        self.assertEqual(f1drivers.build_url(2010, "drivers"), "http://ergast.com/api/f1/2010/drivers.json")


if __name__ == "__main__":
    unittest.main()
