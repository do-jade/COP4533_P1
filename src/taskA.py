import sys

if len(sys.argv) < 2:
    print("Type the following to use: python3 src/taskA.py tests/inputFile.")
    exit(1)

inputFile = sys.argv[1]

try:
    with open(inputFile, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

except FileNotFoundError:
    print("File not found.")
    exit(1)

if not lines:
    print("Empty input file")
    exit(1)

# n = number of hospitals/students
n = int(lines[0])

# Checks if n is a positive integer
if n <= 0:
    print("n must be a positive integer.")
    exit(1)

# Checks if number of lines are right
if len(lines) < (2 * n ) + 1:
    print("Incomplete input file.")
    exit(1)

# Checks edge case for one hospital and one student
if len(lines) == 3:
    print("1 1")
    exit(0)

# Preference lists for hospitals and students
hospitalPreferences = []
studentPreferences = []

# Tracker for free hospitals
freeHospitals = []

# Trackers for matched students and hospitals
matchedHospitals = {}
matchedStudents = {}

# Tracker for next student to propose to
nextProposals = [0] * n

# Adds the preference lists for hospitals and students
for i in range(1, n + 1):
    preferences = list(map(int, lines[i].split()))
    preferences = [p - 1 for p in preferences]
    hospitalPreferences.append(preferences)

for i in range(n + 1, 2 * n + 1):
    preferences = list(map(int, lines[i].split()))
    preferences = [p - 1 for p in preferences]
    studentPreferences.append(preferences)

# Adds the free hospitals
for i in range(n):
    freeHospitals.append(i)

while len(freeHospitals) != 0:
    # Sets the current hospital and student to propose to
    currentHospital = freeHospitals[0]
    studentIndex = nextProposals[currentHospital]

    # Checks if hospital has exhausted their preference list
    if studentIndex >= n:
        freeHospitals.remove(currentHospital)
        continue
    
    # Sets the current student and moves up the proposal list for future.
    currentStudent = hospitalPreferences[currentHospital][studentIndex]
    nextProposals[currentHospital] += 1

    # If current student is free, match
    if currentStudent not in matchedStudents:
        matchedHospitals[currentHospital] = currentStudent
        matchedStudents[currentStudent] = currentHospital
        freeHospitals.remove(currentHospital)

    else:
        # Finds the positions of the current hospital and the matched hospital for current student's preference list
        currentStudentMatch = matchedStudents[currentStudent]
        currentHospitalIndex = studentPreferences[currentStudent].index(currentHospital)
        currentMatchIndex = studentPreferences[currentStudent].index(currentStudentMatch)

        # If current hospital is preferred over current match, delete the original match and add the new one
        if currentHospitalIndex < currentMatchIndex:
            del matchedHospitals[currentStudentMatch]

            matchedHospitals[currentHospital] = currentStudent
            matchedStudents[currentStudent] = currentHospital
            freeHospitals.remove(currentHospital)
            freeHospitals.append(currentStudentMatch)

        # If not, reject the current hospital 
        else:
            continue

# Prints out the result. Added 1 to make up for 0 index code. 
for currentHospital in range(n):
    currentStudent = matchedHospitals[currentHospital]
    print(f"{currentHospital + 1} {currentStudent + 1}")
