cat ../access.log | grep -oE '.*HTTP/1.{2}"' | awk '{print $7}' | sort | uniq -c | sort -nr | head -10 | awk '{printf("%s -- %d\n", $2, $1)}' > ./res.log
