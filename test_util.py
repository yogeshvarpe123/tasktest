import unittest
from util import process_lines
import argparse

class TestLogParser(unittest.TestCase):
    def test_first_lines(self):
        lines = [f"Line {i}\n" for i in range(1, 11)]
        args = argparse.Namespace(first=5, last=None, timestamps=False, ipv4=False, ipv6=False)
        result = process_lines(lines, args)
        self.assertEqual(result, lines[:5])

    def test_last_lines(self):
        lines = [f"Line {i}\n" for i in range(1, 11)]
        args = argparse.Namespace(first=None, last=5, timestamps=False, ipv4=False, ipv6=False)
        result = process_lines(lines, args)
        self.assertEqual(result, lines[-5:])

    def test_timestamps(self):
        lines = ["No timestamp\n", "12:34:56 timestamp\n"]
        args = argparse.Namespace(first=None, last=None, timestamps=True, ipv4=False, ipv6=False)
        result = process_lines(lines, args)
        self.assertEqual(result, ["12:34:56 timestamp\n"])

    def test_ipv4_highlighting(self):
        lines = ["No IP\n", "This is 192.168.0.1\n"]
        args = argparse.Namespace(first=None, last=None, timestamps=False, ipv4=True, ipv6=False)
        result = process_lines(lines, args)
        self.assertIn("\033[92m192.168.0.1\033[0m", result[0])

    def test_ipv6_highlighting(self):
        lines = ["No IP\n", "This is 2001:0db8:85a3:0000:0000:8a2e:0370:7334\n"]
        args = argparse.Namespace(first=None, last=None, timestamps=False, ipv4=False, ipv6=True)
        result = process_lines(lines, args)
        self.assertIn("\033[92m2001:0db8:85a3:0000:0000:8a2e:0370:7334\033[0m", result[0])

if __name__ == "__main__":
    unittest.main()
