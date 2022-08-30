#!/bin/bash
#update file hosts with blacklist

set -u 
set -e

TMPDIR="$(mktemp -d)"
trap 'rm -rf -- "$TMPDIR"' EXIT

pushd $TMPDIR
# download list of lists to download
curl https://v.firebog.net/hosts/lists.php?type=tick -o urls.txt
# gets actual files
xargs -P 2 -n 1 curl -s -O < urls.txt
rm urls.txt
/usr/local/bin/gen_dns_blocklist.py * > /etc/blocked.hosts
systemctl restart dnsmasq
popd

