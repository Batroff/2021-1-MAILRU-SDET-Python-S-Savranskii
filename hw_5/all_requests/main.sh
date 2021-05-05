cat ../access.log | grep -oE '.*HTTP/1.{2}"' | awk '{print $6}' | grep -E '[A-Z]+' | wc -l > ./res.log
