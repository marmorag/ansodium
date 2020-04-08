FROM python:3.7-slim-buster

RUN mkdir -p /ansible/ansible_collections/marmorag/ansodium && \
    mkdir -p /docker

COPY entrypoint.sh /docker/entrypoint.sh

RUN pip install \
        ansible \
        pyyaml \
 && apt update && apt install -y \
        git \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /ansible/ansible_collections/marmorag/ansodium

CMD ['cd /ansible/ansible_collections/marmorag/ansodium && /docker/entrypoint.sh']