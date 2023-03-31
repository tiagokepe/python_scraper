ARG tz="Europe/Madrid"

FROM ubuntu:20.04

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt-get update && \
      apt-get install -y sudo \
            pip \
            python3


COPY . /scraper_code
WORKDIR /scraper_code

ENV DEBIAN_FRONTEND="noninteractive" TZ=${tz}
RUN apt-get install -y tzdata

RUN /scraper_code/scripts/setup-ubuntu.sh

ENTRYPOINT /bin/bash
