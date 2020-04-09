FROM python:3.7-slim-buster

RUN mkdir -p /root/.ansible/collections/ansible_collections/marmorag/ansodium && \
    mkdir -p /docker

COPY entrypoint.sh /docker/entrypoint.sh

RUN pip install \
        ansible \
        pyyaml \
        pynacl \
 && apt update && apt install -y \
        git \
 && rm -rf /var/lib/apt/lists/*

WORKDIR  /root/.ansible/collections/ansible_collections/marmorag/ansodium

CMD /docker/entrypoint.sh