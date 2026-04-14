FROM ubuntu:24.04

WORKDIR /usr/local/wals_analysis

RUN apt-get update && apt-get install -y \
    git \
    moreutils \
    build-essential \
    curl \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

RUN curl -L https://github.com/medialab/xan/releases/download/0.57.0/xan-x86_64-unknown-linux-gnu.tar.gz \
    | tar -xvz \
    && mv xan /usr/local/bin/xan \
    && chmod +x /usr/local/bin/xan


RUN python3 -m venv .venv
ENV PATH="/usr/local/wals_analysis/.venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x ./scripts/prepare_dataset.sh

RUN ./scripts/prepare_dataset.sh fetch
RUN ./scripts/prepare_dataset.sh prune
RUN ./scripts/prepare_dataset.sh join 

EXPOSE 8888

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
