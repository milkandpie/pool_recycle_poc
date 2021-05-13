#!/bin/bash
pipenv run gunicorn -b 0.0.0.0:8085 -w "$1" --threads "$2" app:app -t 300
