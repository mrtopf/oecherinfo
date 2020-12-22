#!/bin/sh

source bin/activate
cd api
export CORONA_SETTINGS=`pwd`/etc/dev.ini
export FLASK_APP=corona
cd ..
