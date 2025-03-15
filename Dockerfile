FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    build-essential \
    texlive-fonts-extra \
    texlive-xetex \
    wget \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# WORKDIR /tmp
# RUN wget https://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz \
#     && zcat < install-tl-unx.tar.gz | tar xf - \
#     && cd install-tl-* \
#     && perl ./install-tl --no-interaction --paper=letter

# ENV PATH=/usr/local/texlive/2024/bin/x86_64-linux:$PATH

WORKDIR /data
COPY Makefile .

RUN make init install
