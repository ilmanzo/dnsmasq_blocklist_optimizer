#!/bin/bash
#update file hosts with blacklist

set -u 
#set -e

TMPDIR="$(mktemp -d)"
trap 'rm -rf -- "$TMPDIR"' EXIT

pushd $TMPDIR
# download list of lists to download
curl https://v.firebog.net/hosts/lists.php?type=tick -o urls.txt
#  gets actual files
wget -q -i urls.txt & 
# in the mean time download other lists
wget -q https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts &
wget -q https://www.github.developerdan.com/hosts/lists/ads-and-tracking-extended.txt &
wget -q https://dbl.oisd.nl/ &
wait
rm urls.txt
# parse and generate blocklist, with filtering and deduplication
/usr/local/bin/gen_dns_blocklist.py * > /etc/blocked.hosts
systemctl restart dnsmasq
popd

