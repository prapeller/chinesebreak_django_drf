FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./app /app
COPY ./requirements.txt /requirements.txt

RUN apk --update add libxml2-dev libxslt-dev libffi-dev libgcc openssl-dev curl
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev

RUN apk add --update --no-cache --virtual .tmp-build-deps \
         gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install --upgrade pip
RUN ls
RUN  pip install -r requirements.txt

WORKDIR /app