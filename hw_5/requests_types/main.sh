cat ../access.log | grep -oE '"[A-Z]{3,7}[[:space:]].*HTTP' | awk '{print substr($1, 2);}' | sort | uniq -c | awk '{printf "%s%s -- %s", sep, $2, $1; sep=", "} END{print ""}' > ./res.log
