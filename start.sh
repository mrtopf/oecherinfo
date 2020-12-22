#!/bin/sh

source bin/activate
cd api
export CORONA_SETTINGS=`pwd`/etc/dev.ini
cd corona
python app.py
