#!/bin/sh
# Create By ifeng
# Web Site:https://www.hicairo.com
# Telegram:https://t.me/HiaiFeng

#定义 UUID 及 伪装路径,请自行修改.(注意:伪装路径以 / 符号开始,为避免不必要的麻烦,请不要使用特殊符号.)
UUID=${UUID:-'de04add9-5c68-8bab-950c-08cd5320df18'}
VMESS_WSPATH=${VMESS_WSPATH:-'/vmess'}
VLESS_WSPATH=${VLESS_WSPATH:-'/vless'}
sed -i "s#UUID#$UUID#g;s#VMESS_WSPATH#$VMESS_WSPATH#g;s#VLESS_WSPATH#$VLESS_WSPATH#g" /etc/v2ray/config.json
sed -i "s#VMESS_WSPATH#$VMESS_WSPATH#g;s#VLESS_WSPATH#$VLESS_WSPATH#g" /etc/nginx/nginx.conf

#如果有设置哪吒探针三个变量,会安装。如果不填或者不全,则不会安装
[ -n "$NEZHA_SERVER" ] && [ -n "$NEZHA_PORT" ] && [ -n "$NEZHA_KEY" ] && wget https://raw.githubusercontent.com/naiba/nezha/master/script/install.sh -O nezha.sh && chmod +x nezha.sh && ./nezha.sh install_agent $NEZHA_SERVER $NEZHA_PORT $NEZHA_KEY
exec "$@"