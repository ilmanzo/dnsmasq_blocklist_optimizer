#!/usr/bin/python3
 
import fileinput

#retrieve all domains in a python list
def getdomains():
    result=[]
    for line in fileinput.input():
        if not line.startswith('0.0.0.0'):
            continue
        domain=line.split()[1] # take the domain part
        result.append(domain)
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
    domains=filter(domains,stage)
    newlen=len(domains)
    if newlen>=curlen:
        break
    curlen=len(domains)
    stage+=1

# output the result in dnsmasq format
domains.sort()
for b in domains:
    if b.count('.')>1:
        print(f"address=/{b}/")
