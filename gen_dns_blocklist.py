#!/usr/bin/python3
 
import fileinput,re

#retrieve all domains in a python list
#TODO filter out ip addresses

ipv4pat = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")

def getdomains():
    result=[]
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
                result.append(domain)
        else:
            result.append(line)
    return result

# reduce domain list, removing an entry if there is already another line
# with the same suffix
# example : 
# if I have an entry with xxx.com, do not add www.xxx.com
# stage is the number of suffixes to consider
def filter(domains,stage):
    blocklist=set()
    domains.sort(key=lambda x: x.count('.'))
    for d in domains:
        tld='.'.join(d.split('.')[-stage:])
        if tld in blocklist:
            pass
            #print(f"pass {stage}, found {tld}, dropped: {d}")
        else:
            blocklist.add(d)
    result=list(blocklist)
    return result


# the reduction process is repeated until the list doesn't shrink anymore
domains=getdomains()
stage=2
curlen=len(domains)
while True:
    print(f"# stage: {stage}, domains: {curlen}")
    domains=filter(domains,stage)
    newlen=len(domains)
    if newlen>=curlen:
        break
    curlen=newlen
    stage+=1

# output the result in dnsmasq format
domains.sort()
for b in domains:
    if b.count('.')>1:
        print(f"address=/{b}/")
