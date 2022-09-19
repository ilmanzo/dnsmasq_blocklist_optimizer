#!/usr/bin/python3
 
import fileinput,re

# domains to NOT block (so don't include in list of blocked domains)
whitelist=[
    re.compile(r'^wl.spotify\.com$'),
    re.compile(r'.*buyon\.it$'),
    re.compile(r'.*survey.alchemer.*$'),
    re.compile(r'app\.simplenote\.com$'),
    re.compile(r'concierge\.analytics\.console\.aws\.a2z\.com$'),        #windows update
    re.compile(r'.*microsoft\.com.*'),  
    re.compile(r'.*\.aws\..+'),
    re.compile(r'.+\.googlevideo\.com$'),
    re.compile(r'^rai-italia.+\.net$'),
    re.compile(r'^cdn.mateti.net$'),
    re.compile(r'^imasdk.googleapis.com$'),
]

blacklist=[
  re.compile(r'.+registry-app.datadoghq.com$'),
]

#retrieve all domains in a python set

ipv4pat = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")

def getdomains():
    result=set()
    for line in fileinput.input():
        line=line.strip()
        if len(line)==0:
            continue
        if line.startswith('#'):
            continue
        if '#' in line:
            pos=line.find('#')
            line=line[:pos].strip()
        domain=line
        if line.startswith('0.0.0.0 ') or line.startswith('127.0.0.1 '):
            domain=line.split()[1] # take the domain part
        if line.startswith('0.0.0.0'):
            domain=line[7:]
        elif line.startswith('127.0.0.1'):
            domain=line[9:]
        domain=domain.strip()
        if '--' in domain or domain.startswith('-') or domain.endswith('-'):
            continue
        if not ipv4pat.match(domain) and domain!="localhost":
            result.add(domain)
    return result


def matchbl(domain):
    for r in blacklist:
        if r.match(domain):
            return True
    return False

def matchwl(domain):
    for r in whitelist:
        if r.match(domain):
            #print(f"{r} matched: {domain}")
            return False
    return True


domains=list(filter(matchwl, getdomains()))

# output the result in /etc/hosts format (more performant than dnsmasq)
# add a line like addn-hosts=/etc/blocked.hosts to your dnsmasq.conf
# where /etc/blocked.hosts is the output of this script
domains.sort(key=len)
for b in domains:
    if '.' in b:
        print(f"0.0.0.0 {b}")
