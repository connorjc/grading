#!/usr/bin/env python3
import csv
import os
import re

CWD = os.getcwd()
DIR_CONTENTS = os.listdir(CWD)

students = dict()
with open("roster.csv",'r') as csvfile:
    for row in csv.DictReader(csvfile):
        students[row["Username"]] = row["Name"]

CWD = os.getcwd() + '/' + max(list(filter(lambda x: "hw" in x ,(filter(os.path.isdir,DIR_CONTENTS)))))
DIR_CONTENTS = os.listdir(CWD)
os.chdir(CWD)

sections = list(filter(os.path.isdir, DIR_CONTENTS))
assert sections, "Execute extract.py first"

with open(CWD+'/'+"GRADES.csv", 'w') as grades:
    gradewriter = csv.writer(grades)
    gradewriter.writerow(["Section", "Name", "Grade"])
    for s in sections:
        grades = []
        comments = sorted(list(filter(lambda x: "_comment" in x, os.listdir(CWD+'/'+s))))
        assert comments, "Execute test.py first"
        for c in comments:
            with open(CWD+'/'+s+'/'+c, 'r') as comment:
                match = re.findall(r'\-(\d+):', comment.read())
                if match:
                    total = 100
                    for g in match:
                        total -= int(g)
                    grades.append([s, students[c.split('_')[0]], total])
                    print(s, c.split('_')[0], "grade:", total)
                else:
                    grades.append([s, students[c.split('_')[0]], 100])
                    print(s, c.split('_')[0], "Full Credit!")
        for g in sorted(grades, key=lambda grade: grade[1]):
            gradewriter.writerow(g)
