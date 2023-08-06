#!/bin/bash


export PYTHONPATH=${PYTHONPATH}:${CI_PROJECT_DIR}
sed -i 's/return parser/args = parser.parse_args()/g' JuMonC/helpers/cmdArguments.py 

python3 /argdown/argdown/argdown.py JuMonC/helpers/cmdArguments.py -f setupParser > ${CI_PROJECT_DIR}/doc/CMD/Parameters.md

ARGDOWN_STATUS=$?

git config --global user.email "c.witzler@fz-juelich.de"
git config --global user.name "auto_doc"

git add doc/CMD/Parameters.md
git commit -m "Documentation for CMD parameters changed"

git push https://gitlab-ci-token:${AUTO_DOC_TOKEN}@${CI_SERVER_HOST}/${CI_PROJECT_PATH}.git HEAD:${CI_COMMIT_REF_NAME}

GITPUSH_STATUS=$?

exit $(( ${ARGDOWN_STATUS} + ${GITPUSH_STATUS} ))

