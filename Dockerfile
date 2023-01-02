FROM nginx:latest
MAINTAINER ifeng <https://t.me/HiaiFeng>
EXPOSE 80
USER root

RUN mkdir /etc/v2ray /usr/local/v2ray

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY nginx.conf /etc/nginx/nginx.conf
COPY config.json /etc/v2ray/
COPY entrypoint.sh /usr/local/v2ray/

RUN apt-get update && apt-get install -y supervisor wget unzip systemctl &&\
    chmod a+x /usr/local/v2ray/entrypoint.sh &&\
    wget -q -O /tmp/v2ray-linux-64.zip https://github.com/v2fly/v2ray-core/releases/download/v4.45.0/v2ray-linux-64.zip &&\
    unzip -d /usr/local/v2ray /tmp/v2ray-linux-64.zip

ENTRYPOINT [ "/usr/local/v2ray/entrypoint.sh" ]
CMD ["/usr/bin/supervisord"]