来自nginx:mainline-alpine-slim
维护者ifeng <https://t.me/HiaiFeng>
曝光 80
用户根

RUN apk update && apk add --no-cache Supervisor wget unzip curl

#定义UUID及伪装路径，请自行修改。（注意：伪装路径以 / 符号开始，为避免不必要的麻烦，请不要使用特殊符号。）
ENV UUID c65063f3-e975-4e13-a860-5feccefb8079
ENV VMESS_WSPATH /vmess
ENV VLESS_WSPATH /vless

复制supervisord.conf /etc/supervisor/conf.d/supervisord.conf
复制nginx.conf /etc/nginx/nginx.conf

运行mkdir /etc/v2ray /usr/local/v2ray
复制config.json /etc/v2ray/
复制入口点.sh /usr/local/v2ray/

#感谢fscarmen大佬提供Dockerfile层优化方案
运行wget -q -O /tmp/v2ray-linux-64.zip https://github.com/v2fly/v2ray-core/releases/download/v4.45.0/v2ray-linux-64.zip && \
    解压 -d /usr/local/v2ray /tmp/v2ray-linux-64.zip v2ray && \
    wget -q -O /usr/local/v2ray/geosite.dat https://github.com/Loyalsoldier/v2ray-rules-dat/releases/latest/download/geosite.dat && \
    wget -q -O /usr/local/v2ray/geoip.dat https://github.com/Loyalsoldier/v2ray-rules-dat/releases/latest/download/geoip.dat && \
    chmod a+x /usr/local/v2ray/entrypoint.sh && \
    apk del wget 解压缩 && \
    rm -rf /tmp/v2ray-linux-64.zip && \
    rm -rf /var/cache/apk/* && \
    rm -rf /tmp/*
    
ENTRYPOINT [ “/usr/local/v2ray/entrypoint.sh” ]
