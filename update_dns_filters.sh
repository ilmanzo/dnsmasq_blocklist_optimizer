#!/bin/bash
#update file hosts with blacklist

set -u 
set -e

TMPDIR="$(mktemp -d)"
trap 'rm -rf -- "$TMPDIR"' EXIT

pushd $TMPDIR
#rm $TMPDIR/*.hosts
curl -s https://hosts.oisd.nl/ -o oisd_nl.hosts & 
curl -s https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/gambling-porn/hosts -o StevenBlack.hosts &
curl -s https://someonewhocares.org/hosts/zero/hosts -o someonewhocares.hosts &
curl -s https://adaway.org/hosts.txt -o adaway.hosts &
curl -s https://s3.amazonaws.com/lists.disconnect.me/simple_ad.txt -o disconnect_me.hosts &
curl -s https://raw.githubusercontent.com/vokins/yhosts/master/hosts -o vokins.hosts &
curl -s https://winhelp2002.mvps.org/hosts.txt -o winhelp2002.hosts &
curl -s https://v.firebog.net/hosts/static/w3kbl.txt -o fireblog.hosts &
curl -s https://v.firebog.net/hosts/neohostsbasic.txt -o neohosts.hosts &
curl -s https://blocklistproject.github.io/Lists/alt-version/ransomware-nl.txt -o ransomware-nl.hosts &
curl -s https://blocklistproject.github.io/Lists/alt-version/gambling-nl.txt -o gambling-nl.hosts &
curl -s https://phishing.army/download/phishing_army_blocklist_extended.txt -o phishing.hosts & 
curl -s https://block.energized.pro/unified/formats/hosts -o energized.hosts & 
#curl -s https://raw.githubusercontent.com/notracking/hosts-blocklists/master/dnsmasq/dnsmasq.blacklist.txt -o /etc/dnsmasq.d/notracking.conf &
wait
/usr/local/bin/gen_dns_blocklist.py *.hosts > /etc/blocked.hosts
systemctl restart dnsmasq
popd

