#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test network and station classes
"""
import warnings
from pathlib import Path
import unittest
import difflib

# Third party  imports

# obsinfo modules
from obsinfo.network import (Station, Network)

warnings.simplefilter("once")
warnings.filterwarnings("ignore", category=DeprecationWarning)
verbose = False


class NetworkTest(unittest.TestCase):
    """
    Class of test methods for network and station objects

    Attributes:
        testing_path (str): path to datafiles to be tested aside from the
            examples
        level (str): level to be printed
        test (boolean): determines if this is test mode
        print_output (boolean): determines if this is print mode. Both can
            coexist.
    """

    def setUp(self, test=True, print_output=False, level=None):
        """
        Set up default values and paths
        """
        self.testing_path = Path(__file__).parent.joinpath("data")

        self.level = level
        self.test = test
        self.print_output = print_output

    def assertTextFilesEqual(self, first, second, msg=None):
        with open(first) as f:
            str_a = f.read()
        with open(second) as f:
            str_b = f.read()

        if str_a != str_b:
            first_lines = str_a.splitlines(True)
            second_lines = str_b.splitlines(True)
            delta = difflib.unified_diff(
                first_lines, second_lines,
                fromfile=first, tofile=second)
            message = ''.join(delta)
            if msg:
                message += " : " + msg
            self.fail("Multi-line strings are unequal:\n" + message)

    def test_read_network_dict(self):
        """Tests reading a network dictionary"""
        station={"site": "bob",
                 "location_code":"00",
                 "locations": 
                    {"00": 
                        {"base": 
                            {"uncertainties.m": {"lat":0, "lon": 0, "elev": 0},
                             "depth.m": 0,
                             "geology":"rock",
                             "vault":"seafloor"
                            },
                        "position":
                            {"lat": 0, "lon": 0, "elev":0
                            }
                        }
                    }
                }
        net_dict = {"network_info": {"code": '4G',
                                     "name": 'test network',
                                     "start_date": "2021-01-01",
                                     "end_date": "2021-01-02",
                                     "description": "Oh what a night!",
                                     },
                    "campaign_ref_name": "HOHO!",
                    "operator": {"full_name": "My park", "reference_name": "INSU-IPGP"},
                    "stations": {"howdy": station.copy(),
                                 "doody": station.copy()}
                   }
        net = Network(net_dict, station_only=True)

def suite():
    return unittest.makeSuite(NetworkTest, 'test')


if __name__ == '__main__':
    unittest.main(defaultTest='suite')

