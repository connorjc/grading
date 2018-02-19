# grading

Atomic python scripts to make grading [C++ Programming for Majors] students' homework submissions less time consuming.

Once `run.x` is executed, various penalties will be enforced, automatically deducting points and listing them in a generated `<username>_comments.txt`.

Traversing through the created directory tree and reviewing the generated output files, diff logs, and source code will enable a much quicker manual grading for the rest of the grading rubric.

After the automatic and manual grading is complete, `grade.py` can be executed to calculate the total grade per student for easy uploading.

* `extract.py` - Only extracts students from a tarball listed in `roster.csv` and organizes them by section.
* `test.py` - Using various input/output files and a `duedate.txt`, the extracted source code is further organized and tested
* `grade.py` - Iterates over all `<username>_comments.txt`, printing the total grade per student in a `GRADES.csv`
* `run.x` - A bash script that executes `extract.py` then `test.py`

[C++ Programming for Majors]: http://www.cs.fsu.edu/~vastola/cop3363/

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them

```sh
python3
```

### Installing

```sh
sudo apt-get install python3
```

#### Test Installation

```sh
python3 --version
```

Should be python3.5+

### Requirements

After installing python3 and cloning the repo, the scripts expect certain files to be included within the grading directory.

#### Files:

`roster.csv` - [example][1]

`duedate.txt` - [example][2]

* First line is the due date for full points.
* Second line is the due date for the late penalty.

`input.txt`

`output.txt`

`<SUBMISSIONS>.tar`

* The submissions within the tarball are expected as `<username>_<assignmentFileName>.cpp`
 * usernames in `roster.csv` should be a subset of those in the files in the tarball

[1]: .roster.csv.example
[2]: .duedate.txt.example

#### Directory Structure

* `hw` directory should contain an integer suffix denoting which assignment it is if more than one `hw` directories exist in the repo.
 * ex: `hw1/  hw2/  hw3/` etc
* `input.txt` and `output.txt` should contain an integer suffix differentiating the test suites and maintaing the mapping of each input file with its output file.
 * ex: `input1.txt  input2.txt  input3.txt ... output1.txt  output2.txt  output3.txt ...`

```sh
grading/
  extract.py
  grade.py
  hw/
    duedate.txt
    input.txt
    example.tar
    output.txt
  roster.csv
  run.x
  test.py
```


## Running

#### Method 1

```sh
./run.x
```

#### Method 2

```sh
./execute.py
./test.py
```

#### Method 3

```python
python3 execute.py
python3 test.py
```

### After manual grading

####Method 1

```sh
./grade.py
```

####Method 2

```python
python3 grade.py
```

## Output

Logging is produced to `stdout` showing at what stage the script is at as well as _anomalies_ such as:

* Late penalties
* Compilation failures and warningsx
* Detected infinite loops

After successful completion of the scripts, several files and directories will be generated within `hw/`:

* `section?/`
 * `?` is substituted with an integer representing a specific section.
* `section?/compiled` - source code that compiles with or without warnings are moved here
* `section?/failed` - source code that **fails** to compile is moved here
* `section?/<username>_comments.txt` - automatically generated but **must be edited during manual grading**
* `GRADES.csv` - generated based on the docked points in the `<username>_comments.txt` files after manual grading  for easy updating of the grade book