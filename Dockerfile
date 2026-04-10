FROM ubuntu:24.04

WORKDIR /usr/local/wals_analysis

# Dependencies
RUN apt-get update && apt-get install -y \
    git \
    moreutils \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Rust environment variables
ENV RUSTUP_HOME=/usr/local/rustup \
    CARGO_HOME=/usr/local/cargo \
    PATH=/usr/local/cargo/bin:$PATH

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
RUN cargo install xan --locked

COPY . .
RUN chmod +x ./scripts/prepare_dataset.sh

RUN ./scripts/prepare_dataset.sh fetch
RUN ./scripts/prepare_dataset.sh prune
RUN ./scripts/prepare_dataset.sh join 

CMD ["bash"]
