#!/bin/bash -x

TAGS=${1:-"fast"}

# Password access helper
PASS="pass NextCairn/mobili_ansible"

# Run with secrets
$PASS | ansible-playbook playbook.yml -i prod --vault-password-file=/bin/cat $@ -t $TAGS
