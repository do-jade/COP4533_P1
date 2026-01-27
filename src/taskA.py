with open('tests/input.txt', 'r') as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

# n = number of hospitals/students
n = int(lines[0])

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
