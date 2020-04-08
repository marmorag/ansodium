FROM python:3.7-slim-buster

RUN mkdir -p /ansible/ansible_collections/marmorag/ansodium
RUN pip install ansible pyyaml
RUN apt update && apt install -y \
    git \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /ansible/ansible_collections/marmorag/ansodium

CMD ansible-test sanity -v --venv --python 3.7 ansodium