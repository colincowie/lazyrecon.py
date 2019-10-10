# lazyrecon.py - made by @th3_protoCOL, inspired by nahmsec
import os
import sys
import urllib3
import argparse
import requests
import subprocess


class LazyRecon():

    # configuration varibles go here
    massdns_path = "/home/recon/tools/massdns"
    massdnsWordlist = "/tools/SecLists/Discovery/DNS/clean-jhaddix-dns.txt"
    chrome_path = "/snap/bin/chromium"
    auquatoneThreads = 5
    # Happy Hunting!

    subdomains = []
    all_urls = []

    def __init__(self):
        print('\033[0;31m'+""" _     ____  ____ ___  _ ____  _____ ____  ____  _
/ \   /  _ \/_   \\\  \///  __\/  __//   _\/  _ \/ \  /|
| |   | / \| /   / \  / |  \/||  \  |  /  | / \|| |\ ||
| |_/\| |-||/   /_ / /  |    /|  /_ |  \__| \_/|| | \||
\____/\_/ \|\____//_/   \_/\_\\\____\\\____/\____/\_/  \\|.py"""+'\033[0m')
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

    # domain discovery
    def discovery(self, output):
        all_urls_file = "./results/"+self.args.domain+"/all_urls.txt"

        print("\033[0;32m[!] Probing for live hosts...\033[0m")

        os.system("cat "+output+" | sort -u | httprobe -p 8080 -c 50 -t 3000 >> "+all_urls_file)
        for url in open(all_urls_file):
            self.all_urls.append(url)
        self.all_urls = sorted(set(self.all_urls))

        print("[*] Found a total of "+str(len(self.all_urls))+" live subdomains")

        with open(all_urls_file, 'w') as f:
            for url in self.all_urls:
                f.write("%s\n" % url)

        # aquatone scan..
        os.system("cat "+all_urls_file+" | aquatone -chrome-path "+self.chrome_path+" -out ./results/"+self.args.domain+"/aqua_out -threads "+str(self.auquatoneThreads)+" -silent")
        # waybackrecon
        # dirsearcher.py intergration!

    def report(self):
        print("...")

    # Main domain scanning function!
    def scan(self):
        print('\033[0;32m'+"[!] Recon started on domain "+self.args.domain+'\033[0m')
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
        self.discovery(output)
        self.report()
        # print some stats here
        print('\033[0;32m'+"[+] Scan for "+self.args.domain+' finished \033[0m')


def main():
    LazyRecon().scan()

if __name__ == "__main__":
    main()
