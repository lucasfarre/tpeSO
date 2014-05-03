#!/bin/bash

python setup.py build
cd ./build/
cd `ls -d lib*`
mv ./cfunctions.so ../../cfunctions.so
rm -r ../../build
