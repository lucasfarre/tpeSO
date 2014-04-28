#!/bin/bash

python setup.py build
cd ./build/
cd `ls -d lib*`
mv ./common/cfunctions.so ../../common/cfunctions.so
rm -r ../../build