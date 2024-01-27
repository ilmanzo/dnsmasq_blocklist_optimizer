#!/usr/bin/python3

import fileinput
import re
import os
import sys


def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


# domains to NOT block (so don't include in list of blocked domains)
with open(os.path.join(get_script_path(), "whitelist.conf"), 'r', encoding='utf-8') as file:
    whitelist = [re.compile(line.strip())
                 for line in file.readlines() if not line.startswith("#")]


ipv4pat = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")


def bad_address(domain):
    if domain.startswith('-') or domain.endswith('-'):
        return True
    if '--' in domain or '-.' in domain:
        return True
    if ipv4pat.match(domain):
        return True
    if domain == "localhost":
        return True
    return False

def cleanup(line):
    if '#' in line:
        pos = line.find('#')
        line = line[:pos].strip()
    domain = line
    if line.startswith('0.0.0.0 ') or line.startswith('127.0.0.1 '):
        # if it has an ip address, take only the domain part
        domain = line.split()[1]
    if line.startswith('0.0.0.0'):
        domain = line[7:]
    elif line.startswith('127.0.0.1'):
        domain = line[9:]
    domain = domain.strip("|^")
    return domain


# retrieve all domains in a python set
def getdomains():
    result = set()
    for line in fileinput.input():
        line = line.strip()
        if len(line) == 0:
            continue
        if line.startswith('#'):
            continue
        domain=cleanup(line)
        if domain in result:  # if we already excluded it, no point to check
            continue
        if bad_address(domain):
            continue
        result.add(domain)
    return result


def matchwl(domain):
    for r in whitelist:
        if r.match(domain):
            #print(f"{r} matched: {domain}")
            return False
    return True


domains = list(filter(matchwl, getdomains()))

# output the result in /etc/hosts format (more performant than dnsmasq)
# add a line like addn-hosts=/etc/blocked.hosts to your dnsmasq.conf
# where /etc/blocked.hosts is the output of this script
domains.sort(key=len)
for b in domains:
    if '.' in b:
        print(f"0.0.0.0 {b}")
