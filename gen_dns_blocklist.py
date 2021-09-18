#!/usr/bin/python3
 
import fileinput,re


# domains to NOT block (so don't include in list of blocked domains)
whitelist=[
    re.compile(r'.*buyon.it$'),
    re.compile(r'.*survey.alchemer.*$'),
    re.compile(r'app.simplenote.com$'),
    re.compile(r'concierge.analytics.console.aws.a2z.com$'),
    re.compile(r'.*\.aws\..*'),
    re.compile(r'.+\-\-.+'),
]


#retrieve all domains in a python set

ipv4pat = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")

def getdomains():
    result=set()
    for line in fileinput.input():
        if line.startswith('#'):
            continue
        line=line.strip()
        if len(line)==0:
            continue
        if '#' in line:
            pos=line.find('#')
            line=line[:pos].strip()
        if line.startswith('0.0.0.0') or line.startswith('127.0.0.1'):
            domain=line.split()[1] # take the domain part
            if not ipv4pat.match(domain) and domain!="localhost":
                result.add(domain)
        else:
            result.add(line)
    return result



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
domains.sort()
for b in domains:
    if b.count('.')>1:
        #print(f"address=/{b}/")
        print(f"0.0.0.0 {b}")
