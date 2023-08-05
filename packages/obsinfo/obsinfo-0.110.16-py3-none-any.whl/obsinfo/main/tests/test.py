#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test StationXML creation
"""
from pathlib import Path
import glob
import unittest
import inspect
# from pprint import pprint
import xml.etree.ElementTree as ET
from .CompareXMLTree import XmlTree
import warnings

from obsinfo.main.makeStationXML import main as make_StationXML
from obsinfo.misc.discoveryfiles import (Datapath)


warnings.simplefilter("once")
warnings.filterwarnings("ignore", category=DeprecationWarning)
verbose = False

     
class StationXMLTest(unittest.TestCase):
    """
    Class of test methods for StationXML creation
    """

    """
    Test suite for obsinfo operations.
    """
    def setUp(self):
        self.testing_path = Path(__file__).parent / "data"
        self.infofiles_path = (Path(__file__).resolve().parents[2]
                               / "_examples" / 'Information_Files')

    def test_makeSTATIONXML(self):
        """
        Test STATIONXML creation.
        """
        for fname in ["SPOBS.INSU-IPGP.network.yaml",
                      "BBOBS.INSU-IPGP.network.yaml"]:
            net_file = str(self.infofiles_path / "network" / fname)
            make_StationXML([net_file, '--quiet'],
                             Datapath(str(self.infofiles_path)))

            compare = XmlTree()
            # excluded elements
            excludes = ["Created", "Real", "Imaginary", "Numerator",
                        "CreationDate", "Description", "Module"]
            excludes_attributes = ["startDate", "endDate"]
            excludes = [compare.add_ns(x) for x in excludes]

            for stxml in glob.glob("*.xml"):
                xml1 = ET.parse(stxml)
                xml2 = ET.parse(self.testing_path / "StationXML" / stxml)
                self.assertTrue(compare.xml_compare(
                    compare.getroot(xml1), compare.getroot(xml2),
                    excludes=excludes,
                    excludes_attributes=excludes_attributes))
                Path(stxml).unlink()


def suite():
    return unittest.makeSuite(StationXMLTest, 'test')


if __name__ == '__main__':
    unittest.main(defaultTest='suite')

