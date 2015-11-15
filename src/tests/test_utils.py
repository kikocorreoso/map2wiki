"""
Tests for utils module
"""

import os
import sys
import unittest
import warnings
warnings.filterwarnings('always')

path = os.path.abspath(os.path.join('..'))
sys.path.append(path)

from utils import get_address, isolate_name, get_wiki_info

class UtilsTest(unittest.TestCase):
    
    def test_get_address(self):
        """Tests for `get_address` function."""
        result = get_address(-1.81602098644987, 52.5487429714954)
        expected = {
            "place_id":"73626440",
            "licence":"Data © OpenStreetMap contributors, ODbL 1.0. http://www.openstreetmap.org/copyright",
            "osm_type":"way",
            "osm_id":"90394420",
            "lat":"52.54877605",
            "lon":"-1.81627023283164",
            "display_name":"137, Pilkington Avenue, Castle Vale, Maney, Birmingham, West Midlands, England, B72 1LH, United Kingdom",
            "address":{
                "house_number":"137",
                "road":"Pilkington Avenue",
                "suburb":"Castle Vale",
                "hamlet":"Maney",
                "city":"Birmingham",
                "state_district":"West Midlands",
                "state":"England",
                "postcode":"B72 1LH",
                "country":"United Kingdom",
                "country_code":"gb"
            }
        }
        self.assertEqual(result['place_id'], expected['place_id'])
        self.assertEqual(result['address']['house_number'], 
                     expected['address']['house_number'])
        self.assertEqual(result['licence'], expected['licence'])
        self.assertEqual(sorted(result.keys()), sorted(expected.keys()))
        
        result = get_address(-40, 40)
        expected = {'NoDataError': 'No data on this location'}
        self.assertEqual(result, expected)
        
        result = get_address(-40,40, service = 'kk')
        expected = {'URLError': 'Cannot connect to URL'}
        self.assertEqual(result, expected)
        
    def test_isolate_name(self):
        """Tests for `isolate_name` function."""
        # Right now, tests are only for spanish names
        names = ['Calle de la PyConES',
                 'Avenida del Rey Kiko I',
                 'Paseo de los Torpedos',
                 'Vía de las PyLadies',
                 'Calle de Python']
        expected = ['pycones', 'rey kiko i', 'torpedos', 
                    'pyladies', 'python']
        for n, e in zip(names, expected):
            result = isolate_name(n)
            expected = e
            self.assertEqual(result, expected)
    
    def test_get_wiki_info(self):
        """Tests for the `get_wiki_info` function."""
        result = get_wiki_info('Python')
        self.assertEqual(result.url, 
                         'https://es.wikipedia.org/wiki/Python')
        self.assertEqual(result.title, 'Python')
        result = get_wiki_info('Javascripttttttt')
        self.assertTrue(isinstance(result, str))

if __name__ == "__main__":
    unittest.main(verbosity = 2)
