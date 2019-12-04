# lazyrecon.py - made by @th3_protoCOL, inspired by nahmsec
import os
import sys
import urllib3
import argparse
import requests
import subprocess
try:
    from slack import RTMClient
except:
    pass

class LazyRecon():

    # configuration varibles go here
    massdns_path = "/home/recon/tools/massdns"
    massdnsWordlist = "/tools/SecLists/Discovery/DNS/clean-jhaddix-dns.txt"
    chrome_path = "/snap/bin/chromium"
    dirsearchWordlist="dirsearch/db/dicc.txt"
    dirsearchThreads = 50
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
        try:
           slack.RTMClient.run_on(event="message")(self.bot_listen)
           self.slack_data = {
                'token': os.environ.get('SLACK_BOT_TOKEN'),
                'channel': 'GQ3PDJRL0',
                'as_user': True,
                'text': 'default'
           }
        except:
            pass
    # Parse script arguments
    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser(description="LazyRecon automates some tasks of reconnaissance.")
        parser.add_argument('-d', '--domain', help="Domain to scan", required=False)
        parser.add_argument('-e','--exclude', help="Specify excluded domains", required=False)
        parser.add_argument('-b','--bot', help="Start slack bot", action='store_true')
        args = parser.parse_args()
        return args

    # To do: verify all tools are downloaded!
    def dependencies(self):
        print("...")

    # domain discovery
    def discovery(self, output):
        all_urls_file = "./results/"+self.args.domain+"/all_urls.txt"

        print("\033[0;32m[!] Probing for live hosts...\033[0m")

        os.system("cat "+output+" | sort -u | httprobe -p 8080 -c 50 -t 3000 | sort -u >> "+all_urls_file)
        for url in open(all_urls_file):
            self.all_urls.append(url)

        self.all_urls = sorted(set(self.all_urls))
        with open(all_urls_file, 'w') as f:
            for url in self.all_urls:
                f.write("%s" % url)
        print("[*] Found a total of "+str(len(self.all_urls))+" live subdomains")
        if(self.args.bot):
            self.slack_data['text'] = 'Found a total of '+str(len(self.all_urls))+' live urls'
            requests.post(url='https://slack.com/api/chat.postMessage',data=self.slack_data)
            data = {
                'token': os.environ.get('SLACK_BOT_TOKEN'),
                'title': self.args.domain,
                'channels': 'GQ3PDJRL0',
                'content': self.all_urls}
            response = requests.post(url='https://slack.com/api/files.upload',data=data)
            print(response.content)

        # aquatone scan..
        os.system("cat "+all_urls_file+" | aquatone -chrome-path "+self.chrome_path+" -out ./results/"+self.args.domain+"/aqua_out -threads "+str(self.auquatoneThreads)+" -silent")
        # waybackrecon
        os.system("cat "+all_urls_file+" | waybackurls > ./results/"+self.args.domain+"/wayback.txt")

        # dirsearcher.py
        os.system("python3 dirsearch/dirsearch.py -e php,asp,aspx,jsp,html,zip,jar -w "+self.dirsearchWordlist+" -L "+all_urls_file+" -t "+str(self.dirsearchThreads)+" --random-agents  --plain-text-report ./results/"+self.args.domain+"/dirsearch.txt")
        try:
            self.slack_data['text'] = 'Recon finished'
            requests.post(url='https://slack.com/api/chat.postMessage',data=self.slack_data)
        except:
            pass

    def report(self):
        print("...")

    # Main domain scanning function!
    def scan(self):
	# Clear discovered
        self.all_urls = []
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

        if self.args.bot:
            self.slack_data['text'] = 'Found '+str(sub_count)+' urls!'
            requests.post(url='https://slack.com/api/chat.postMessage',data=self.slack_data)
        self.discovery(output)
        self.report()
        # print some stats here
        print('\033[0;32m'+"[+] Scan for "+self.args.domain+' finished \033[0m')

    def bot_listen(self, **payload):
        data = payload['data']
        web_client = payload['web_client']
        rtm_client = payload['rtm_client']
        message = data.get('text',[])
        if 'scan' in message:
            if 'http' in message:
            	domain = message.split('|')[1][:-1]
            else:
                domain = message.split(' ')[1]
            channel_id = data['channel']
            web_client.chat_postMessage(
                channel=channel_id,
                text="Your recon on "+domain+" will start shortly"
            )
            self.args.domain = domain
            self.scan()

    def slack_bot(self):
        print('\033[0;32m'+"[!] Starting slack bot!\033[0m")
        try:
            self.slack_data['text'] = 'Ready for action!'
       	    requests.post(url='https://slack.com/api/chat.postMessage',data=self.slack_data)
            rtm_client = RTMClient(token=os.environ.get('SLACK_BOT_TOKEN'))
            rtm_client.start()
        except:
            pass
def main():
    recon = LazyRecon()
    if recon.args.bot:
        recon.slack_bot()
    else:
        recon.scan()

if __name__ == "__main__":
    main()
