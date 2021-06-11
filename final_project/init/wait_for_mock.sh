#!/bin/bash

while [[ "$(curl -o /dev/null -s -w "%{http_code}\n" http://vk_mock:8090/is_alive)" != "200" ]]; do
  echo waiting for mock...;
  sleep 3;
done;

echo mock is up;
