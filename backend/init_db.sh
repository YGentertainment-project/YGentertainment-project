#! /bin/bash
set -x

if [[ ! -f manage.py ]]; then
    echo "No manage.py, wrong location"
    exit 1
fi

sleep 2
docker rm -f yg-mariadb-dev
docker run -it -d -e MYSQL_DB=ygenter -e MYSQL_USER=ygenter -e MYSQL_PASSWORD=ygenter -p 127.0.0.1:3306:3306 --name yg-mariadb-dev mariadb:10.7.1

if [ "$1" = "--migrate" ]; then
    sleep 3
    echo `cat /dev/urandom | head -1 | md5sum | head -c 32` > data/config/secret.key
    python manage.py migrate
    python manage.py inituser --username root --password rootroot --action create_super_admin
fi
