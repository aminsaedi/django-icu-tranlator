# Stage 1: Build Python environment
FROM alpine AS build-python

ENV PYTHONUNBUFFERED=1
ENV TZ=America/Toronto
ENV PIP_BREAK_SYSTEM_PACKAGES 1

RUN apk add --update --no-cache \
    python3 \
    git \
    tzdata \
    bash \
    nodejs \
    npm \
    python3-dev \
    wget \
    gcc \
    make \
    zlib-dev \
    libffi-dev \
    openssl-dev \
    musl-dev \
    py3-pip

RUN ln -sf python3 /usr/bin/python \
    && git config --global user.name "Docker Bot" \
    && git config --global user.email "bot@orangedigital.com"

# RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools pytz tzdata
# RUN pip install pytz tzdata --upgrade
# RUN pip install tzdata --upgrade

# Stage 2: Copy application code and dependencies
FROM build-python AS app

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /app

# ENV DJANGO_ENV=production
# RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["sh", "./startapp.sh"]
