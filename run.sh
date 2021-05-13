#!/bin/bash
pipenv run gunicorn -b 0.0.0.0:8085 -w 2 --threads 0 app:app -t 300
