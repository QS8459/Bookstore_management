FROM alpine:latest

RUN apk --no-cache update sudo bash && \
    apk add nano \
    postgresql15 postgresql15-contrib postgresql15-openrc postgresql15-client libpq su-exec tzdata\
    postgresql-url_encode && \
    rm -rf /var/cache/apk/* && \
    mkdir /docker-entrypoint-initdb.d

RUN addgroup -S bookstore && adduser bookstore -S -G bookstore bookstore

RUN echo "bookstore:admin" |chpasswd

RUN echo "bookstore ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

ENV LANG en_GB.utf8
ENV PGDATA /var/lib/postgresql/data

VOLUME /var/lib/postgresql/data

COPY docker-entrypoint.sh /

ENTRYPOINT ["/docker-entrypoint.sh"]

EXPOSE 5432

RUN chmod -R 755 /docker-entrypoint.sh && \
    mkdir -p /run/postgresql && \
    chown postgres: /run/postgresql


# USER postgres

WORKDIR /home/bookstore

CMD ["postgres"]