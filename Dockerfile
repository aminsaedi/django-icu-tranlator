FROM alpine

ENV PYTHONUNBUFFERED=1
ENV TZ=America/Toronto

RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN apk add --update --no-cache git
RUN apk add --no-cache tzdata
RUN apk add --no-cache bash
RUN apk add --update --no-cache nodejs npm
RUN apk add python3-dev
RUN apk add --update --no-cache \
    wget \
    gcc \
    make \
    zlib-dev \
    libffi-dev \
    openssl-dev \
    musl-dev

RUN git config --global user.name "Docker Bot"
RUN git config --global user.email "bot@orangedigital.com"


RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
RUN pip install pytz --upgrade
RUN pip install tzdata --upgrade

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt


COPY . /app

ENV DJANGO_ENV=production
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["sh", "./startapp.sh"]


