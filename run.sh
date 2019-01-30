#!/bin/bash

# get greatest numbered homework directory
hw=$( printf '%s\n' hw[0-9]* | sort --version-sort | tail -n 1)

# if a zipfile is found & there is no tarball then call format 
if [ -f $hw/submissions.zip ] && [ ! -f $hw/*.tar ]; then
    ./format.py
fi

# attempt to extract a tarball
./extract.py

# if extraction is successfull test the submissions
if [ $? -eq 0 ]; then
    ./test.py
fi
