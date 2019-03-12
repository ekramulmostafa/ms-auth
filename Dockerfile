FROM python:3.7-alpine

RUN adduser -D service

WORKDIR /home/service

COPY requirements.txt requirements.txt
RUN apk add --no-cache --update \
    git \
    bash \
    libffi-dev \
    openssl-dev \
    bzip2-dev \
    zlib-dev \
    readline-dev \
    build-base \
    postgresql-dev
RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt

COPY app app
COPY migrations migrations
COPY manage.py wsgi.py .flaskenv boot.sh test.sh lint.sh .flake8 .pylint ./
RUN chmod +x boot.sh

RUN chown -R service:service ./
USER service

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]