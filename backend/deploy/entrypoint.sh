#!/bin/sh

DATA=/data

mkdir -p $DATA/log $DATA/config $DATA/public/avatar $DATA/public/website

if [ ! -f "$DATA/config/secret.key" ]; then
    echo $(cat /dev/urandom | head -1 | md5sum | head -c 32) > "$DATA/config/secret.key"
fi

python3 manage.py makemigrations
python3 manage.py migrate --no-input

python3 manage.py runserver 0.0.0.0:8000 --insecure
