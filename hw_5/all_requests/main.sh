cat ../access.log | grep -E 'POST|GET|HEAD|PUT|DELETE|CONNECT|OPTIONS|TRACE|PATCH' | wc -l > ./res.log
