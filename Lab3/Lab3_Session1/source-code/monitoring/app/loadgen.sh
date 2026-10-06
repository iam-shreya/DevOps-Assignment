#!/bin/sh
# Generates traffic so that the dashboards show live data
while true; do
  wget -q -O /dev/null http://demo-app:8000/ 2>/dev/null
  wget -q -O /dev/null http://demo-app:8000/order 2>/dev/null
  [ $((RANDOM % 5)) -eq 0 ] && wget -q -O /dev/null http://demo-app:8000/missing 2>/dev/null
  sleep 0.3
done
