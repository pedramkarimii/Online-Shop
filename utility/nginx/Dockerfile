FROM nginx:stable-alpine

USER root

RUN apk add --update openssl bash

COPY ./default-ssl.conf.template /etc/nginx/default-ssl.conf.template
COPY ./default.conf.template /etc/nginx/default.conf.template
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]