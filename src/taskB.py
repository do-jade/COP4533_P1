# NOT FINISHED OR RUNNABLE
# FILE IS JUST PSEUDOCODE FOR THE PURPOSE OF ENSURING LOGIC WORKS BEFORE IMPLEMENTING

# Helper Functions
# Parses A Line Into Ints
# https://www.w3schools.com/python/python_try_except.asp
# https://www.w3schools.com/python/ref_string_strip.asp
def lineToInts(givenLine):
    pieces = givenLine.split()
    if not pieces:
        return []
    try:
        return [int(x) for x in pieces]
    except ValueError:
        raise ValueError("Non Int In Line: '" + givenLine.strip() + "'")

# Checks If Provided Input Is A Valid Permutation
# They Should Be Correct Length, In The Range Of 1 To n And No Dupes
def validPermutationCheck(toCheck, n):
    if len(toCheck) != n:
        return False
    checked = [False] * n
    for val in toCheck:
        if val < 1 or val > n:
            return False
        temp = val - 1
        if checked[temp]:
            return False
        checked[temp] = True
    return True

# Originally Used Multiple Times, But Easier To Keep As Functions

# Rank Tables During Comparison
# studentRank Ends Up As The Position Of The Hospital In The Students Preference List
def createRankingTable(n, studentPref):
    studentRanks = [[-1] * n for _ in range(n)]
    for student in range(n):
        for posit, hospital in enumerate(studentPref[student]):
            studentRanks[student][hospital] = posit
    return studentRanks

# Checks For Blocking Pairs
# Returns True When Stable And (False, "hospital student") Otherwise
def blockingPairCheck(n, hospitalToStudent, studentToHospital, hospitalPreference, studentRanks):
    for hospital in range(n):
        matchedStudent = hospitalToStudent[hospital]

        # Only Students With A Higher Rank Than matchedStudent Can Create A Blocking Pair
        for student in hospitalPreference[hospital]:
            if student == matchedStudent:
                break

            # If Student Ranks Higher Than Their Current Hospital
            currentMatch = studentToHospital[student]
            if studentRanks[student][hospital] < studentRanks[student][currentMatch]:
                return False, str(hospital + 1) + " " + str(student + 1)
    return True, ""

# Main
if __name__ == "__main__":
    # Will Go Invalid As Soon As Something Fails
    try:
        # Read Preference File
        with open("tests/input.txt", "r") as f:
            preferences = [line.strip() for line in f if line.strip()]

        # Check For Empty File Edge Case
        if not preferences:
            raise ValueError("Preference File Is Empty")

        # Take First Line And Designate N
        try:
            n = int(preferences[0])
        except ValueError:
            raise ValueError("n Needs To Be The First Line")

        # Check For n Being Valid
        if n <= 0:
            raise ValueError("n Has To Be Positive")

        #print("DEBUG n:", n)
        #print("DEBUG len(preferences):", len(preferences))
        #print("DEBUG [repr(x) for x in preferences]:", [repr(x) for x in preferences])

        # Verify Input File Has Correct Number Of Lines
        totalInputLines = 1 + 2 * n
        if len(preferences) != totalInputLines:
            raise ValueError("Incorrect Number Of Input Lines, Should Be: " + str(totalInputLines) + ". Instead Got: " + str(len(preferences)))

        # Go Through Hospital Preferences
        hospitalPreference = []
        for hospitalIndex in range(n):
            temp = lineToInts(preferences[1 + hospitalIndex])

            if not validPermutationCheck(temp, n):
                raise ValueError("Hosptial Preferences Are Not Valid Permutations, Index: " + str(hospitalIndex + 1))

            # 0 Indexing
            hospitalPreference.append([x - 1 for x in temp])

        # Go Through Student Preferences
        studentPreference = []
        for studentIndex in range(n):
            temp = lineToInts(preferences[1 + n + studentIndex])

            if not validPermutationCheck(temp, n):
                raise ValueError("student prefs not a permutation at student " + str(studentIndex + 1))

            # 0 Indexing
            studentPreference.append([x - 1 for x in temp])

        # Read Matching Verification File
        #with open("tests/matching.txt", "r") as f:
        #    matches = [line.strip() for line in f if line.strip()]
        # https://stackoverflow.com/questions/4655250/difference-between-utf-8-and-utf-16
        # FOR SOME REASON THIS HAS TO ACCOUNT FOR BOTH FILE VERSIONS DO NOT REMOVE THE UTF 16 PART PLEASE
        try:
            with open("tests/matching.txt", "r", encoding="utf-8") as f:
                matches = [line.strip() for line in f if line.strip()]
        except UnicodeDecodeError:
            with open("tests/matching.txt", "r", encoding="utf-16") as f:
                matches = [line.strip() for line in f if line.strip()]

        #print("DEBUG n =", n)
        #print("DEBUG len(matches) =", len(matches))
        #print("DEBUG [repr(x) for x in matches]", [repr(x) for x in matches])
        #with open("tests/matching.txt", "rb") as bf:
        #    print("DEBUG bf.read(30) =", bf.read(30))

        # Number Of Matches Should Match n
        if len(matches) != n:
            raise ValueError("Incorrect Number Of Matching Input Lines, Should Be: " + str(n) + ". Instead Got: " + str(len(matches)))

        hospitalToStudent = [-1] * n
        studentToHospital = [-1] * n
        for line in matches:
            matchingPair = lineToInts(line)

            # Check Matching Input
            if len(matchingPair) != 2:
                raise ValueError("Match Line Should Only Have 2 Ints: '" + line + "'")
            pairHospital, pairStudent = matchingPair
            hospitalIndex = pairHospital - 1
            studentIndex = pairStudent - 1

            # Validate Individual Pair
            if not (0 <= hospitalIndex < n) or not (0 <= studentIndex < n):
                raise ValueError("Pair Is Not Valid: " + str(pairHospital) + " " + str(pairStudent))

            # Check For Uniqueness
            if hospitalToStudent[hospitalIndex] != -1:
                raise ValueError("Hospital " + str(pairHospital) + " Is Matched Multiple Times")
            if studentToHospital[studentIndex] != -1:
                raise ValueError("Student " + str(pairStudent) + " Is Matched Multiple Times")
            hospitalToStudent[hospitalIndex] = studentIndex
            studentToHospital[studentIndex] = hospitalIndex

        # Ensure Everyone Is Matched
        for hospitalIndex in range(n):
            if hospitalToStudent[hospitalIndex] == -1:
                raise ValueError("Hospital " + str(hospitalIndex + 1) + " Is Not Matched")
        for studentIndex in range(n):
            if studentToHospital[studentIndex] == -1:
                raise ValueError("Student " + str(studentIndex + 1) + " Is Not Matched")

    # If Unable To Locate File
    except FileNotFoundError as err:
        print("INVALID (File Not Found: " + str(err) + ")")
        raise SystemExit(0)
    
    # Value Errors
    except ValueError as err:
        print("INVALID (" + str(err) + ")")
        raise SystemExit(0)

    # Find Blocking Pairs
    studentRanks = createRankingTable(n, studentPreference)
    result = blockingPairCheck(n, hospitalToStudent, studentToHospital, hospitalPreference, studentRanks)

    # Print Results
    if result[0]:
        print("VALID STABLE")
    else:
        print("UNSTABLE (Blocking Pair: " + result[1] + ")")