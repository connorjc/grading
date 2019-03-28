#!/usr/bin/env python3
'''
    COP3014 compatibility module
    This module will rename every file in the zip and tarball them 
        into expected format

    For this course the submissions must be downloaded in mass via canvas.

    Canvas provides homeworks as a zip file with a different naming convention 
        than expected in the COP3363 course
        ex.
        COP3014: lnamefname_<late>_timestamp_timestamp_<filename>.cpp
        COP3363: username_<filename>.cpp
        
        * Timestamps are also not preserved in the zipfile so they must be 
            spoofed to preserve compatibility.
'''
import os
import subprocess
import csv
import re
import zipfile
import tarfile

#STEP 1: Load students' names from my roster
my_students = dict()
with open("roster.csv", 'r') as roster:
    reader = csv.DictReader(roster)
    for row in reader:
        name = row["Name"]
        name = re.sub('[, -]','',name).lower()
        my_students[name] = row["Username"]

#STEP 2: Enter hw dir
CWD = os.getcwd()
DIR_CONTENTS = os.listdir(CWD)
hw_dir = list(filter(lambda x: "hw" in x ,(filter(os.path.isdir,DIR_CONTENTS))))
assert hw_dir, "Must have a hw dir"
hw_dir = max(hw_dir)+'/'
CWD = os.getcwd() + '/' + hw_dir
DIR_CONTENTS = os.listdir(CWD)
os.chdir(CWD)

#STEP 3: Unpack zipfile of EVERY student
print("Unpacking zipfile")
zip_name = list(filter(lambda x: ".zip" in x,DIR_CONTENTS))
assert zip_name, "Must upload zipfile containing hw submissions"
zip_name = zip_name[0]
with zipfile.ZipFile(zip_name,"r") as zip_ref:
    zip_ref.extractall(zip_name[:-4])

#STEP 4: Set timestamp of each submission & rename files
print("Setting timestamp of each submission & renaming files")
#STEP 4.1: Get duedate
due_time = ""
late_time = ""
with open("duedate.txt", 'r') as duedate:
    match = re.match(r'\d{4}-(\d\d)-(\d\d)',duedate.readline()[:-1])
    due_time = match.group(1)+match.group(2)+"1200"
    match = re.match(r'\d{4}-(\d\d)-(\d\d)',duedate.readline()[:-1])
    late_time = match.group(1)+match.group(2)+"1200"

#STEP 4.2: find my students files 
files = os.listdir(CWD+zip_name[:-4])
for f in files:
    match = re.match(r'(\w*?)_(late_)?(\d*_){,}(.*?.cpp)',f)
    orig_file = match.group(0)
    name = match.group(1)
    late = False if match.group(2) is None else True
    source_code = match.group(4)
    if name in my_students.keys():
        new_file = my_students[name] + '_' + source_code
        cmd = "mv " + orig_file + ' ' + new_file
        subprocess.run(cmd, cwd=CWD+zip_name[:-4], shell=True)

        cmd = "touch -t "
        cmd += late_time if late else due_time
        cmd += ' ' + new_file
        subprocess.run(cmd, cwd=CWD+zip_name[:-4], shell=True)

#STEP 5: Tar reformatted submissions
print("Constructing tarball")
files = os.listdir(CWD+zip_name[:-4])
tar_name = hw_dir[:-1]+"_sub.tar"
with tarfile.open(tar_name, 'w') as tar:
    for f in files:
        tar.add(CWD+zip_name[:-4]+'/'+f, arcname=f)

#STEP 6: Clean up
print("Removing extracted directory")
cmd = "rm -rf " + zip_name[:-4]
subprocess.run(cmd, cwd=CWD, shell=True)
