FROM redis:latest


COPY /home/guilherme/teste_scrapy_rev3/redis/redis.conf /usr/local/etc/redis/redis.conf


EXPOSE 6379


CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]