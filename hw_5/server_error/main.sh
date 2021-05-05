cat ../access.log | grep -oE '.*HTTP/1.{4}5[0-9]{2}' | awk '{print $1}' | sort | uniq -c | sort -k1 -nr | head -5 | awk '{printf "%s -- %s\n", $1, $2}' > ./res.log
