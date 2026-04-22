FROM ubuntu:24.04

WORKDIR /usr/local/wals_analysis

# Installa ansible
RUN apt-get update && apt-get install -y \
  ansible \
  && rm -rf /var/lib/apt/lists/*

COPY . .

RUN ansible-playbook ./ansible/playbook.yml -c local
RUN chmod +x ./scripts/*.sh

RUN ./scripts/fetch.sh -y
RUN ./scripts/prune.sh
RUN ./scripts/join.sh

EXPOSE 8888

ENV PATH="/usr/local/wals_analysis/.venv/bin:$PATH"

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
