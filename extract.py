#!/usr/bin/env python3
""" Extract latest tar and sort by recitation(s)
    Expects tar, directory, roster to already be uploaded
"""
import csv
import os
import tarfile


BLUE = "\033[1;34m" #light blue
NC = "\033[0m"

CWD = os.getcwd()
DIR_CONTENTS = os.listdir(CWD)

assert "roster.csv" in DIR_CONTENTS, "Must have csv containing students: Username, Name, Recitation"

# gather the names of the latest hw, tar, and sections
hw_dir = list(filter(lambda x: "hw" in x ,(filter(os.path.isdir,DIR_CONTENTS))))
assert hw_dir, "Must have a hw dir"
hw_dir = max(hw_dir)+'/'
print("Using directory:", BLUE, hw_dir, NC)

roster = dict() #roster[username] = section
with open("roster.csv", 'r') as csvfile:
    for row in csv.DictReader(csvfile):
        roster[row["Username"]] = row["Section"]
    # mkdirs for each section
    sections = set(roster.values())
    for s in sections:
        try:
            os.makedirs(hw_dir+s+"/failed")
            print("Creating directory:", hw_dir+s+"/failed")
        except FileExistsError:
            print("Directory", hw_dir+s+"/failed", "already exists")

        try:
            os.makedirs(hw_dir+s+"/compiled")
            print("Creating directory:", hw_dir+s+"/compiled")
        except FileExistsError:
            print("Directory", hw_dir+s+"/compiled" ,"already exists")

CWD = os.getcwd() + '/' + hw_dir
DIR_CONTENTS = os.listdir(CWD)
os.chdir(CWD)

tar_name = list(filter(lambda x: ".tar" in x,DIR_CONTENTS))
assert tar_name, "Must upload tarball containing hw submissions"
tar_name = tar_name[0]
print("Using assignment archive:", BLUE, tar_name, NC)

with tarfile.open(tar_name, 'r') as tar:
    # extract only my students from tar into corresponding directories
    for username in sorted(roster.keys()):
        section = roster[username]
        for tarinfo in tar:
            if username in tarinfo.name:
                tar.extract(tarinfo.name, path=section)
                print("Unpacking archive:", section, tarinfo.name)
