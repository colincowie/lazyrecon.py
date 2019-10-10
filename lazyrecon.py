# lazyrecon.py - made by @th3_protoCOL, inspired by nahmsec
import os
import sys
import urllib3
import argparse
import requests

class LazyRecon():

    # configuration varibles go here
    massdns_path = "/home/recon/tools/massdns"
    massdnsWordlist = "/tools/SecLists/Discovery/DNS/clean-jhaddix-dns.txt"
    # Happy Hunting!

    subdomains = []

    def __init__(self):
        print('\033[0;31m'+""" _     ____  ____ ___  _ ____  _____ ____  ____  _
/ \   /  _ \/_   \\\  \///  __\/  __//   _\/  _ \/ \  /|
| |   | / \| /   / \  / |  \/||  \  |  /  | / \|| |\ ||
| |_/\| |-||/   /_ / /  |    /|  /_ |  \__| \_/|| | \||
\____/\_/ \|\____//_/   \_/\_\\\____\\\____/\____/\_/  \\|"""+'\033[0m')
        urllib3.disable_warnings()
        self.args = LazyRecon.parse_args()

    # Parse script arguments
    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser(description="LazyRecon automates some tasks of reconnaissance.")
        parser.add_argument('-d', '--domain', help="Domain to scan", required=True)
        parser.add_argument('-e','--exclude', help="Specify excluded domains", required=False)
        args = parser.parse_args()
        return args

    # To do: verify all tools are downloaded!
    def dependencies(self):
        print("...")
    # NameServer records function
    def nsrecords(self):
        if os.path.exists(self.massdns_path):
            os.system(+self.massdns_path+"/bin/massdns -r "+self.massdns_path+"lists/resolvers.txt -t A -q -o S > results/"+self.args.domain+"/mass.txt")
            #todo: massdns subbrute
        else:
            print("[-] Could not find massdns directory")
        # grep for CNAMEs and NXDOMAIN
        print("...")

    # domain discovery
    def discovery(self):
        # probe for live host (httprobe -c 50 -t 300)
            # append results to urllist.txt
        # aquatone scan..
        # waybackrecon
        # dirsearcher.py intergration!
        print("...")

    def report(self):
        print("...")

    # Main domain scanning function!
    def scan(self):
        print('\033[0;32m'+"Recon started on domain "+self.args.domain+'\033[0m')
        path = "results/"+self.args.domain
        if not os.path.exists(path):
            os.makedirs(path)
        output = path+"/"+self.args.domain+".txt"
        print("Listing subdomains using findomain...")
        os.system("findomain -t "+self.args.domain+" -u "+output)
        if os.path.exists(output):
            sub_count = sum(1 for line in open(output))
        else:
            sub_count = 0
        print("[*] Found "+str(sub_count)+" urls")
        self.nsrecords()
        self.discovery()
        self.report()
        # print some stats here
        print('\033[0;32m'+"Scan for "+self.args.domain+' finished \033[0m')


def main():
    LazyRecon().scan()

if __name__ == "__main__":
    main()
