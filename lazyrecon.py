# lazyrecon.py - made by @th3_protoCOL, inspired by nahmsec
import sys
import urllib3
import argparse
import requests
from subdomain3.brutedns import Brutedomain

class LazyRecon():

    subdomains = []

    # configuration varibles will go here

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
        # check crt.sh with massdns/scripts/ct.py
        # Massdns
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
        print("Listing subdomains using Brutedomain...")
        # subdomain3 passes args into the main function... Can I do this in a more logical way?
        sub_params = argparse.ArgumentParser(
            description='A new generation of tool for discovering subdomains( ip , cdn and so on),version=3.0')
        sub_params.add_argument('-s', '--speed', default="low",
                            help='low,medium and high')
        sub_params.add_argument("-d", "--domain",
                            help="domain name,for example:baidu.com")
        sub_params.add_argument(
            "-l",
            "--level",
            default=2,
            type=int,
            help="example: 1,hello.baidu.com;2,hello.world.baidu.com")
        sub_params.add_argument("-f", "--file",
                            help="One domain each line")
        sub_params.add_argument("-ns", "--default_dns", default='n',
                            help="If you want use default dns,set it y,otherwise set n(It will automatically discover the fastest nameserver) ")
        sub_params.add_argument("-c", "--cname",
                            help="Collect cname of subdomain and save to result/cname.txt,you can add it to cdn.txt when you find it is cdn ,y or n",
                            default='y')
        sub_params.add_argument("-f1", "--sub_file",
                            help="sub dict", default='dict/sub_full.txt')
        sub_params.add_argument("-f2", "--next_sub_file",
                            help="next_sub dict", default='dict/next_sub_full.txt')
        sub_params.add_argument("-f3", "--other_file",
                            help="Subdomain log from other tools,such as search engine")

        sub_params.domain = self.args.domain
        sub_params.cname = 'y'
        sub_params.level = 1
        sub_params.speed = 'high'
        sub_params.sub_file = 'subdomain3/dict/sub_full.txt'
        sub_params.default_dns = 'y'
        sub_params.next_sub_file = 'subdomain3/dict/next_sub_full.txt'
        sub_params.other_file = None
        sub_brute = Brutedomain(sub_params)
        sub_brute.run()
        sub_brute.collect_cname()

        # use findomain
        print("Checking certspotter...")
        get_subdomains = requests.get("https://api.certspotter.com/v1/issuances?domain="+self.args.domain+'&include_subdomains=true&expand=dns_names',verify = False)
        subdomain_page = get_subdomains.text.split('"dns_names":[')
        print('Parsing subdomains')
        for page in subdomain_page[1:]:
            page_list = page.split('],')[0].split(',')
            for page2 in page_list:
                self.subdomains.append(page2.split('"')[1])
        print("[*] Found "+str(len(self.subdomains))+" subdomains.")
        for domain in self.subdomains:
            print(domain)

        # check certspotter using request
        # curl -s https://certspotter.com/api/v0/certs\?domain\=$domain | jq '.[].dns_names[]' | sed 's/\"//g' | sed 's/\*\.//g' | sort -u | grep $domain >> ./$domain/$foldername/$domain.txt
        self.nsrecords()
        self.discovery()
        self.report()
        # print some stats here
        print('\033[0;32m'+"Scan for "+self.args.domain+' finished \033[0m')


def main():
    LazyRecon().scan()

if __name__ == "__main__":
    main()
