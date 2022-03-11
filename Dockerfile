FROM python:3.8-alpine3.13

WORKDIR /usr/src/app

COPY . .

RUN chmod 775 ./entry.sh

EXPOSE 8000

CMD ["sh", "-c", "./entry.sh"]