#!/bin/bash

printf "Populating database, please wait for the end of this process.\n"

printf "\nLoading action fixtures...\n"
python3 manage.py loaddata post/fixtures/actions.json

printf "\nLoading addresses fixtures...\n"
python3 manage.py loaddata core/fixtures/addresses.json

printf "\nLoading base users fixtures...\n"
python3 manage.py loaddata user/fixtures/users.json

printf "\nLoading contact fixtures...\n"
python3 manage.py loaddata user/fixtures/contacts.json

printf "\nLoading initial tweets...\n"
python3 manage.py loaddata post/fixtures/posts.json

printf "\nFixture loading finished, enjoy!\n"