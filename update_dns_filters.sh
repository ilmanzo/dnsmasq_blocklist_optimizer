#!/bin/sh
#update file hosts with blacklist
cd /tmp
curl https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/gambling-porn/hosts -o StevenBlack.hosts &
curl https://someonewhocares.org/hosts/zero/hosts -o someonewhocares.hosts &
curl https://adaway.org/hosts.txt -o adaway.hosts &
curl https://s3.amazonaws.com/lists.disconnect.me/simple_ad.txt -o disconnect_me.hosts &
curl https://raw.githubusercontent.com/vokins/yhosts/master/hosts -o vokins.hosts &
curl https://winhelp2002.mvps.org/hosts.txt -o winhelp2002.hosts &
curl https://v.firebog.net/hosts/static/w3kbl.txt -o fireblog.hosts &
curl https://v.firebog.net/hosts/neohostsbasic.txt -o neohosts.hosts &
wait
/usr/local/bin/gen_dns_blocklist.py *.hosts > /etc/dnsmasq.d/blocklist.conf 
#cp /etc/hosts.original /etc/hosts
#grep '^0\.0\.0\.0' /tmp/hosts >> /etc/hosts
systemctl restart dnsmasq
rm /tmp/*.hosts
