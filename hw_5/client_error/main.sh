cat ../access.log | grep -oE '.*HTTP/1.{4}4[0-9]{2}[[:space:]][0-9]+' | awk '{print $1, $9, $10, $7}' | sort -k3 -rn | head -5 > ./res.log
