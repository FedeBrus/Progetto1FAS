FROM ubuntu:24.04

WORKDIR /usr/local/wals_analysis

RUN apt-get update && apt-get install -y \
    git \
    moreutils \
    curl \
    && rm -rf /var/lib/apt/lists/*

ARG XAN_VERSION=v0.1.1

RUN curl -L "https://github.com/geoffroy-aubry/xan/releases/download/${XAN_VERSION}/xan-linux-x86_64" -o /usr/local/bin/xan \
    && chmod +x /usr/local/bin/xan

COPY prepare_dataset.sh ./
RUN chmod +x prepare_dataset.sh

RUN ./prepare_dataset.sh fetch
RUN ./prepare_dataset.sh prune
RUN ./prepare_dataset.sh join 

CMD ["bash"]
