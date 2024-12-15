#!/usr/bin/env python3

import argparse
import re
import sys

class CustomHelpFormatter(argparse.HelpFormatter):
    def _get_help_string(self, action):
        """Customize help string to exclude default values."""
        return action.help  # Return the help text without the default info

    def _format_action_invocation(self, action):
        """Customize action invocation to show options with '=NUM'."""
        if action.option_strings:
            options = ', '.join(action.option_strings)
            if action.metavar:
                return f"{options}={action.metavar}"  # Add '=NUM' explicitly
            return options
        return super()._format_action_invocation(action)
        

def parse_args():
    parser = argparse.ArgumentParser(
        prog='./util.py',
        usage='./util.py [OPTION]... [FILE]',
        add_help=False,
        formatter_class=CustomHelpFormatter
    )
    parser.add_argument("-h", "--help", action="help", help="Print help")
    parser.add_argument("file", nargs="?", type=argparse.FileType('r'), default=sys.stdin, help=argparse.SUPPRESS)
    parser.add_argument("-f", "--first", type=int, metavar="NUM", help="Print first NUM lines")
    parser.add_argument("-l", "--last", type=int, metavar="NUM", help="Print last NUM lines")
    parser.add_argument("-t", "--timestamps", action="store_true", help="Print lines that contain a timestamp in HH:MM:SS format")
    parser.add_argument("-i", "--ipv4", action="store_true", help="Print lines containing IPv4 addresses, with matches highlighted")
    parser.add_argument("-I", "--ipv6", action="store_true", help="Print lines that contain an IPv6 address (standard notation), matching IPs are highlighted")
    return parser.parse_args()

def highlight(text, regex):
    return re.sub(regex, lambda m: f"\033[92m{m.group(0)}\033[0m", text)

def process_lines(lines, args):
    if args.first:
        lines = lines[:args.first]
    if args.last:
        lines = lines[-args.last:]
    
    if args.timestamps:
        lines = [line for line in lines if re.search(r"\b\d{2}:\d{2}:\d{2}\b", line)]
    if args.ipv4:
        ipv4_regex = r"\b((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\.){3}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\b"
        lines = [highlight(line, ipv4_regex) for line in lines if re.search(ipv4_regex, line)]
    if args.ipv6:
        ipv6_regex = r"\b(([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}|::)\b"
        lines = [highlight(line, ipv6_regex) for line in lines if re.search(ipv6_regex, line)]
    
    return lines

def main():
    args = parse_args()
    with args.file as f:
        lines = f.readlines()
    
    result = process_lines(lines, args)
    for line in result:
        print(line, end="")

if __name__ == "__main__":
    main()
