FROM python:3.10.8 AS base

RUN apt-get update
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN apt-get -y install libasound-dev portaudio19-dev libportaudiocpp0
RUN apt-get install portaudio19-dev

FROM base AS app

WORKDIR /usr/src/app
COPY pyproject.toml .
RUN pip install -e .

COPY . .
CMD python -m pytest
