COP4533 Programming Assignment 1

Team Members:
Dohyun Lee (UFID: 92659157)
Charan Sriram (UFID: 73870076)

Project Structure

How to Run

Task A:
1. Add a file to tests folder for input
2. Run the following command: 
    - python3 src/taskA.py tests/inputFilename

Example using preexisting input file: 
- python3 src/taskA.py tests/input.txt

This should output the answer.

Task B:
There are two options for running Task B.
1. You can pipe the output for task A into tests/outputFilename as shown below:
    - python src/taskA.py tests/inputFilename > tests/outputFilename
    - python src/taskB.py tests/inputFilename tests/outputFilename
2. If you are running just Task B without Task A, then you have to manually edit the input and output files first and then run:
    - python src/taskB.py tests/inputFilename tests/outputFilename

Example following the same structure as before:
- python src/taskA.py tests/input.txt > tests/output.txt
- python src/taskB.py tests/input.txt tests/output.txt

This will print VALID STABLE or INVALID (message)

Task C:
![Task C Graph](data/task_C_graph.png)
We used the Measure-Command { command } in windows powershell to time Task A and Task B running through n From 1 to 512 in 2^n increments.
This command has a little variability in measured times, however it is able to produce overall accurate and viewable results that show an exponential growth trend for both Task's executions as n becomes increasingly large.