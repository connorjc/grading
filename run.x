#!/bin/bash

./extract.py

if [ $? -eq 0 ]; then
    ./test.py
fi
