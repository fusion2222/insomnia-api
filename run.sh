#!/bin/bash

if [ ! -d ./.venv ]; then
	echo "[+] Setting up Virtualenv..."
    virtualenv .venv
fi

source ./.venv/bin/activate
pip install -r requirements.txt

if [[ $1 == 'dev' ]]; then
	export FLASK_ENV=development
else
	export FLASK_ENV=production
fi

export FLASK_APP=urls.py
flask run
