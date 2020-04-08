#!/usr/bin/env bash

if [[ -z ${TEST_TYPE+x} ]]; then
    echo "Env variable TEST_TYPE is undefined, provide either 'sanity' or 'playbook' value."
    exit 1
fi

if [[ ${TEST_TYPE} == "sanity" ]]; then
    exit $(ansible-test sanity -v --venv --python 3.7 ansodium)
elif [[ ${TEST_TYPE} == "playbook" ]]; then
    exit $(ansible tests/main.yml)
fi