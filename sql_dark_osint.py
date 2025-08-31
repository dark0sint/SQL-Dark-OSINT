#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
import requests
from bs4 import BeautifulSoup
from termcolor import colored
import argparse
import multiprocessing
import google

def banner():
    print(colored("""
  ____  ____    _    ____    _    ____   ___  _   _ 
 / ___||  _ \  / \  |  _ \  / \  |  _ \ / _ \| \ | |
 \___ \| | | |/ _ \ | | | |/ _ \ | | | | | | |  \| |
  ___) | |_| / ___ \| |_| / ___ \| |_| | |_| | |\  |
 |____/|____/_/   \_\____/_/   \_\____/ \___/|_| \_|
                                                  
    SQL Dark OSINT Scanner
    """, "cyan"))

def scan_url(url):
    try:
        r = requests.get(url, timeout=5)
        if "You have an error in your SQL syntax" in r.text or "mysql_fetch" in r.text:
            print(colored("[VULN] SQL Injection found: " + url, "red"))
        else:
            print(colored("[SAFE] " + url, "green"))
    except Exception as e:
        print(colored("[ERROR] " + url + " - " + str(e), "yellow"))

def search_dork(dork, engine):
    print(colored("[*] Searching dork: " + dork + " on " + engine, "blue"))
    urls = []
    if engine == "google":
        for url in google.search(dork, num=20, stop=20, pause=2):
            urls.append(url)
    # Add other search engines if needed
    return urls

def osint_gather(url):
    print(colored("[*] Gathering OSINT data for: " + url, "magenta"))
    # Placeholder for OSINT functionality
    # For example, gather headers, DNS info, etc.
    try:
        r = requests.get(url)
        print(colored("Title: " + BeautifulSoup(r.text, "html.parser").title.string, "magenta"))
    except:
        print(colored("Failed to gather OSINT data", "yellow"))

def main():
    banner()
    parser = argparse.ArgumentParser(description="SQL Dark OSINT Scanner")
    parser.add_argument("-d", "--dork", help="SQLi dork to search")
    parser.add_argument("-e", "--engine", default="google", help="Search engine to use (default: google)")
    parser.add_argument("-t", "--target", help="Target URL for scanning")
    parser.add_argument("--osint", action="store_true", help="Gather OSINT data")
    args = parser.parse_args()

    if args.dork:
        urls = search_dork(args.dork, args.engine)
        pool = multiprocessing.Pool(10)
        pool.map(scan_url, urls)
    elif args.target:
        if args.osint:
            osint_gather(args.target)
        else:
            scan_url(args.target)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
