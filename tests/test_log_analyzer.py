"""
test_log_analyzer.py — Unit test for post-flight CanSat log analyzer.
"""

import unittest
import os
import tempfile
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tools")))
from log_analyzer import analyze_log


class TestLogAnalyzer(unittest.TestCase):
    def setUp(self):
        # Create a sample flight log in temporary file
        self.tmp = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv")
        self.tmp.write("Time,Temp,Pressure,Altitude,AccelX,AccelY,AccelZ,GyroX,GyroY,GyroZ,Lat,Lon,GPSAlt,Sats\n")
        self.tmp.write("1.0,25.0,1013.25,10.0,0.0,0.0,1.0,0.0,0.0,0.0,12.9716N,77.5946E,900,8\n")
        self.tmp.write("2.0,24.5,1008.10,55.0,0.2,0.1,2.5,0.1,0.2,0.0,12.9718N,77.5948E,945,8\n")
        self.tmp.write("3.0,24.0,1002.00,105.0,0.1,-0.1,1.1,0.0,0.0,0.0,12.9720N,77.5950E,995,9\n")
        self.tmp.close()

    def tearDown(self):
        if os.path.exists(self.tmp.name):
            os.remove(self.tmp.name)

    def test_log_metrics(self):
        result = analyze_log(self.tmp.name)
        self.assertEqual(result["total_samples"], 3)
        self.assertEqual(result["valid_samples"], 3)
        self.assertEqual(result["corrupt_rows"], 0)
        self.assertEqual(result["duration_seconds"], 2.0)
        self.assertEqual(result["altitude_m"]["apogee"], 105.0)
        self.assertEqual(result["altitude_m"]["launch_alt"], 10.0)
        self.assertEqual(result["altitude_m"]["apogee_gain"], 95.0)
        self.assertEqual(result["gps_fixes_logged"], 3)
        self.assertAlmostEqual(result["temperature"]["avg"], 24.5)


if __name__ == "__main__":
    unittest.main()
