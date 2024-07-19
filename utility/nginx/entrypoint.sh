#!/bin/bash

set -e

echo "Checking for dhparams.pem"
if [ ! -f "/vol/proxy/ssl-dhparams.pem" ]; then
  echo "ssl-dhparams.pem does not found, creating ..."
  openssl dhparam -out /vol/proxy/ssl-dhparams.pem 1024
fi

echo "Checking for fullchain.pem"
if [ ! -f "/etc/letsencrypt/live/onlineshoppedramkarimi.ir/fullchain.pem" ]; then
  echo "No SSL certification, HTTP Mode Enabled !"
  cat /etc/nginx/default.conf.template > /etc/nginx/conf.d/default.conf
else
  echo "SSL cert exists, HTTPS Mode Enabled !"
  cat /etc/nginx/default-ssl.conf.template > /etc/nginx/conf.d/default.conf
fi

nginx-debug -g "daemon off;"