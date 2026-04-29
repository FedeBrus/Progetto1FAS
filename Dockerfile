FROM ubuntu:24.04

WORKDIR /usr/local/wals_analysis

RUN apt-get update \
    && apt-get install -y ansible \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN ansible-playbook -i ./ansible/hosts ./ansible/jupyter.yml -c local

RUN apt-get purge -y ansible
RUN chmod +x ./scripts/*.sh
RUN ./scripts/fetch.sh -y && ./scripts/prune.sh && ./scripts/join.sh


EXPOSE 8888
ENV PATH="/usr/local/wals_analysis/.venv/bin:$PATH"
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
