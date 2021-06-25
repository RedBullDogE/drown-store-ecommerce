FROM python:3.8-alpine

RUN python -m pip install --upgrade pip

COPY . /app
WORKDIR /app
RUN mv ./entrypoint.sh /

ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1

RUN apk update
RUN apk add --virtual build-deps \
        libressl-dev \
        postgresql-dev \
        libffi-dev \
        gcc \
        musl-dev \
        python3-dev \
        zlib-dev \
        jpeg-dev
RUN apk add postgresql-libs libjpeg

RUN pip install -r requirements.txt
RUN apk del build-deps

ENTRYPOINT ["sh", "/entrypoint.sh"]