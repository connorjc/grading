#!/usr/bin/env python3
import csv
import os
import shlex
import subprocess
""" Attempts to compile all the students submissions, organizing the
    source code and resutling files into failed/compiled directories.
    Diff output from executables.
"""
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
inputs = sorted(list(filter(lambda i: "input" in i, (filter(os.path.isfile, DIR_CONTENTS)))))
assert inputs, "Must create input files"

outputs = sorted(list(filter(lambda i: "output" in i, (filter(os.path.isfile, DIR_CONTENTS)))))
assert outputs, "Must create output files"

test_files = list(zip(inputs, outputs))

assert "duedate.txt" in DIR_CONTENTS, "Must create duedate file"

source_code = dict() 
assert sections, "Execute extract.py first"
for s in sections:
    source = list(filter(lambda x: ".cpp" in x,os.listdir(CWD+'/'+s)))
    assert source, "Execute extract.py first"
    source_code[s] = source

for section, submissions in source_code.items():
    print(section)
    with open("duedate.txt", 'r') as due:
        due_date = due.readline()
        late_date = due.readline()
        cmd = 'find ./*.cpp -newermt \"' + due_date.strip() + '\" ! -newermt \"' + late_date.strip() + '\"'
        for cpp in subprocess.run(cmd, cwd=CWD+'/'+section, shell=True, stdout=subprocess.PIPE).stdout.split():
            cpp = (str(cpp)[4:].split('_')[0])
            print("LATE PENALTY:", cpp)
            with open(CWD+'/'+section+'/'+cpp+"_comments.txt", 'w') as comment:
                print("-10:\tlate penalty (up to 24 hours)", file=comment)
        cmd = 'find ./*.cpp -newermt \"' + late_date + '\"'
        for cpp in subprocess.run(cmd, cwd=CWD+'/'+section, shell=True, stdout=subprocess.PIPE).stdout.split():
            cpp = (str(cpp)[4:].split('_')[0])
            print("BEYOND LATE PENALTY:", cpp)
            with open(CWD+'/'+section+'/'+cpp+"_comments.txt", 'w') as comment:
                print("BEYOND LATE PENALTY:", file=comment)

    for code in submissions:
        cmd = ["g++", code, "-o", code[:-4]+".x"]
        with open(CWD+'/'+section+'/'+code[:-4]+'.err', 'a') as err ,\
                open(CWD+'/'+section+'/'+code.split('_')[0]+"_comments.txt", 'a') as comment:
            if subprocess.run(cmd, cwd=CWD+'/'+section, stdout=err, stderr=subprocess.STDOUT).returncode == 0:
                #Compile success: mv source & exectuable to compiler dir
                if(os.path.getsize(CWD+'/'+section+'/'+code[:-4]+'.err') > 0):
                    print("Compilation warnings: ", code)
                    print("-5:\tcompilation errors",file=comment)
                else:
                    print("Compilation successful: ", code)
                print("\n\n*\n\nGraded by: Connor Christian",file=comment)
                cmd = ["mv", code, code[:-4]+".x", code[:-4]+".err", "compiled/."]
                subprocess.run(cmd, cwd=CWD+'/'+section)
            else:#Compile failure: mv source & err to fail dir
                print("Compilation failed: ", code)
                print("-5:\tcompilation failed (-5 per fix up to 10 errors)", file=comment)
                print("\n\n*\n\nGraded by: Connor Christian",file=comment)
                cmd = ["mv", code, code[:-4]+".err", "failed/."]
                subprocess.run(cmd, cwd=CWD+'/'+section)
    # iterate over compiled source code and run it, testing the output
    for x in sorted(list(filter(lambda i: ".x" in i, os.listdir(CWD+'/'+section+'/compiled')))):
        count = 0
        print("Executing", x)
        for i,o in test_files:
            count += 1
            with open(CWD+'/'+section+'/compiled/'+x[:-2]+str(count)+'.out', 'w') as out,\
                open(i,'r') as I, open(CWD+'/'+section+'/compiled/'+x[:-2]+str(count)+'.diff', 'w') as diff:
                cmd = ["./"+x]
                try:
                    subprocess.run(cmd, cwd=CWD+'/'+section+'/compiled', \
                        stdin=I, stdout=out, stderr=subprocess.STDOUT, \
                        timeout=10)
                    #cmd = ["diff", "-bBs", CWD+'/'+o, CWD+'/'+section+'/compiled/'+x[:-2]+str(count)+'.out']
                    #cmd = shlex.split("diff -Bbis --suppress-common-lines " + CWD+'/'+o + ' ' + CWD+'/'+section+'/compiled/'+x[:-2]+str(count)+'.out')
                    cmd = shlex.split("tput cols")
                    width = int(subprocess.check_output(cmd))
                    cmd = shlex.split("diff -Bbisy -W " + str(width) + " --suppress-common-lines " + CWD+'/'+o + ' ' + CWD+'/'+section+'/compiled/'+x[:-2]+str(count)+'.out')
                    subprocess.run(cmd, cwd=CWD+'/'+section+'/compiled', stdout=diff)
                except subprocess.TimeoutExpired:
                    print("INFINITE LOOP DETECTED")
                    with open(CWD+'/'+section+'/compiled/'+x[:-2]+'.err', 'a') as err:
                        print("INFINITE LOOP DETECTED", file=err)
                    break
        #mkdir for with students name and move all files into it
        try:
            os.mkdir(CWD+'/'+section+'/compiled/'+students[x.split('_')[0]])
            print("Creating directory:", CWD+'/'+section+'/compiled/\''+students[x.split('_')[0]]+'\'')
        except FileExistsError:
            print("Directory", CWD+'/'+section+'/compiled/\''+students[x.split('_')[0]]+'\'' ,"already exists")
        cmd = ["mv "+x[:-2]+'* \''+students[x.split('_')[0]]+"\'/."]
        subprocess.run(cmd, cwd=CWD+'/'+section+'/compiled', shell=True)
