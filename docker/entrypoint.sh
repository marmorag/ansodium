#!/usr/bin/env bash

if [[ -z ${TEST_TYPE+x} ]]; then
    echo "Env variable TEST_TYPE is undefined, provide either 'sanity' or 'playbook' value."
    exit 1
fi

if [[ ${TEST_TYPE} == "sanity" ]]; then
    ansible-test sanity -v --venv --python 3.7 ansodium
    exit $?
elif [[ ${TEST_TYPE} == "playbook" ]]; then
    ansible-playbook tests/main.yml
    exit $?
fi

echo "Unknown value : ${TEST_TYPE}"
exit 1