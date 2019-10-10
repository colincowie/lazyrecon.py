```
  _     ____  ____ ___  _ ____  _____ ____ ____  _
 / \   /  _ \/_   \\  \///  __\/  __//   _Y  _ \/ \  /|
 | |   | / \| /   / \  / |  \/||  \  |  / | / \|| |\ ||
 | |_/\| |-||/   /_ / /  |    /|  /_ |  \_| \_/|| | \||
 \____/\_/ \|\____//_/   \_/\_\\____\\____|____/\_/  \|.py

```

## Usage

`pythom3 lazyrecon.sh -d target.com`

## About

This is a custom python port of [lazyrecon](https://github.com/nahamsec/lazyrecon), it is intended to automate some tedious tasks of reconnaissance and information gathering.
This tool allows you to gather some information that should help you identify what to do next and where to look.

## Tools Used
1. [findomain](https://github.com/Edu4rdSHL/findomain)
2. [httprobe](https://github.com/tomnomnom/httprobe)
3. [aquatone](https://github.com/michenriksen/aquatone)
4. [waybackurls](https://github.com/tomnomnom/waybackurls)
5. [dirsearch](https://github.com/maurosoria/dirsearch)

## Installation
1. Install required tools
2. `pip install -r requirements.txt`

## Development to do:
- aquatone (in-progress)
- waybackurls
- dirsearch
- subbrute.py
- Report generation
- SlackBot
- test or remove massdns
- _Explore Python Replacement for current tools_

**Warning:** This code was originally created for personal use, it generates a substantial amount of traffic, please use with caution.
