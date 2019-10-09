# lazyrecon.py - made by @th3_protoCOL, inspired by nahmsec
import sys
import argparse

class LazyRecon():

    # configuration varibles will go here

    def __init__(self):
        print(
        """ _     ____  ____ ___  _ ____  _____ ____  ____  _
/ \   /  _ \/_   \\\  \///  __\/  __//   _\/  _ \/ \  /|
| |   | / \| /   / \  / |  \/||  \  |  /  | / \|| |\ ||
| |_/\| |-||/   /_ / /  |    /|  /_ |  \__| \_/|| | \||
\____/\_/ \|\____//_/   \_/\_\\\____\\\____/\____/\_/  \\|""")
        self.args = LazyRecon.parse_args()

    # Parse script arguments
    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser(description="LazyRecon automates some tasks of reconnaissance.")
        parser.add_argument('-d', '--domain', help="Domain to scan", required=True)
        parser.add_argument('-e','--exclude', help="Specify excluded domains", required=False)
        args = parser.parse_args()
        return args

    # NameServer records function
    def nsrecords(self):
        # check crt.sh with massdns/scripts/ct.py
        # Massdns
        # grep for CNAMEs and NXDOMAIN
        print("todo")

    # domain discovery
    def discovery(self):
        # probe for live host (httprobe -c 50 -t 300)
            # append results to urllist.txt
        # aquatone scan..
        # waybackrecon
        # dirsearcher.py intergration!
        print("todo")

    def report(self):
        print("todo")

    # Main domain scanning function!
    def scan(self):
        print("Recon started on domain "+ self.args.domain)
        print("Listing subdomains using findomain...")
        # use findomain
        print("Checking certspotter...")
        # check certspotter using request
        # curl -s https://certspotter.com/api/v0/certs\?domain\=$domain | jq '.[].dns_names[]' | sed 's/\"//g' | sed 's/\*\.//g' | sort -u | grep $domain >> ./$domain/$foldername/$domain.txt
        self.nsrecords()
        self.discovery()
        self.report()
        # print some stats here


def main():
    LazyRecon().scan()

if __name__ == "__main__":
    main()
