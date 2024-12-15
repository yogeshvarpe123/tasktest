#!/usr/bin/env python3

import argparse
import re
import sys

def parse_args():
    parser = argparse.ArgumentParser(
        description="Log Parsing Utility v1.01"
    )
    parser.add_argument("file", nargs="?", type=argparse.FileType('r'), default=sys.stdin, help="Input file or stdin")
    parser.add_argument("-f", "--first", type=int, help="Print first NUM lines")
    parser.add_argument("-l", "--last", type=int, help="Print last NUM lines")
    parser.add_argument("-t", "--timestamps", action="store_true", help="Print lines containing timestamps (HH:MM:SS)")
    parser.add_argument("-i", "--ipv4", action="store_true", help="Print lines containing IPv4 addresses, with matches highlighted")
    parser.add_argument("-I", "--ipv6", action="store_true", help="Print lines containing IPv6 addresses, with matches highlighted")
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
        ipv4_regex = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
        lines = [highlight(line, ipv4_regex) for line in lines if re.search(ipv4_regex, line)]
    if args.ipv6:
        ipv6_regex = r"\b([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b"
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
