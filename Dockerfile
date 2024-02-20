ARG PYTHON_VERSION=3.9.6
FROM python:${PYTHON_VERSION}-slim as base

WORKDIR /app
COPY . /app

RUN pip3 install -r requirements.txt

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]