#!/bin/bash

echo "Stoping old version"
if [ -d /root/web ];
then
    cd web
    make stop
    cd ..
fi

echo "Pulling new version"
rm -rf /root/web
git clone git@github.com:kosyachniy/web.git
if [ -d /root/data/web ];
then
    echo ""
else
    cp -r /root/web/data /root/data/web
fi

echo "Copying keys"
cp /root/.secrets/web.env /root/web/.env

echo "Starting new version"
make run
