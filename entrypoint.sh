#!/bin/sh
# Create By ifeng
# Web Site:https://www.hicairo.com
# Telegram:https://t.me/HiaiFeng

sed -i "s/UUID/$UUID/g" /etc/v2ray/config.json
sed -i "s/VMESS_WSPATH/$VMESS_WSPATH/g" /etc/v2ray/config.json
sed -i "s/VLESS_WSPATH/$VLESS_WSPATH/g" /etc/v2ray/config.json
sed -i "s/VMESS_WSPATH/$VMESS_WSPATH/g" /etc/nginx/nginx.conf
sed -i "s/VLESS_WSPATH/$VLESS_WSPATH/g" /etc/nginx/nginx.conf
exec "$@"