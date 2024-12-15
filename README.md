Interview app - log parsing utility v1.01:

This is a simple Python utility for parsing and filtering log files. It allows you to extract specific lines based on timestamps, IPv4/IPv6 addresses, or line counts.

Usage
./util.py [OPTION]... [FILE]

Options:
-f, --first NUM  : Print the first NUM lines.
-l, --last NUM   : Print the last NUM lines.
-t, --timestamps : Print lines containing timestamps (HH:MM:SS).
-i, --ipv4       : Print lines with IPv4 addresses (highlighted).
-I, --ipv6       : Print lines with IPv6 addresses (highlighted).

Examples:

1)Print the first 10 lines:
python ./util.py -f 10 test_0.log

2)Print the last 10 lines:
python ./util.py -l 10 test_0.log

3)print lines with IPv4 addresses:
python ./util.py --ipv4 test_0.log

4)print lines with IPv6 addresses:
python ./util.py --ipv6 test_0.log

5)print lines with timestamps addresses:
python ./util.py -t test_0.log



Testing

Run the test suite using unittest:
python -m unittest test_util.py

Files
util.py : The main log parsing script.
test_util.py : Unit tests for the utility.
test_0.log : Example log file for testing.