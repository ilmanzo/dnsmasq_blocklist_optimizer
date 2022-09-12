#!/bin/bash
#update file hosts with blacklist

set -u 
#set -e

TMPDIR="$(mktemp -d)"
trap 'rm -rf -- "$TMPDIR"' EXIT

pushd $TMPDIR
wget -q https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts &
wget -q https://www.github.developerdan.com/hosts/lists/ads-and-tracking-extended.txt &
wget -q https://dbl.oisd.nl/ &
# download list of lists to download
curl https://v.firebog.net/hosts/lists.php?type=tick -o urls.txt
# gets actual files
for u in $(cat urls.txt); do wget -q $u ; done
wait
rm urls.txt
/usr/local/bin/gen_dns_blocklist.py * > /etc/blocked.hosts
systemctl restart dnsmasq
popd

