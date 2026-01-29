# NOT FINISHED OR RUNNABLE
# FILE IS JUST PSEUDOCODE FOR THE PURPOSE OF ENSURING LOGIC WORKS BEFORE IMPLEMENTING

# Helper Functions
# Read The File And Return A List Of Non-Empty Lines
def readNonEmptyLines(filepath):
    data = read_all_lines(filepath)
    lineList = []
    for line in data:
        temp = trim(line)
        if temp != "":
            lineList.append(temp)
    return lineList

# Parses A Line Into Ints
def intsFromLine(inp):
    # Shed The Whitespace
    pieces = split_whitespace(n)
    intList = []
    for piece in pieces:
        # Will Probably Need An Edge Case
        intList.append(to_int(piece))
    return intList

# Checks If Provided Input Is A Valid Permutation
def validPermutation(givenValues, n):
    if len(givenValues) != n:
        return False
    checked = [False] * n
    for x in givenValues:
        if x < 1 or x > n:
            return False
        if checked[x - 1]:
            return False
        checked[x - 1] = True
    return True

# Might Need To Use More Than Once So I Made Them Functions

# Rank Tables During Comparison
def createRankingTable(n, studentPreference):
    # rankStudent[stud][hosp] = position of hospital in student's preference list
    rankStudent = [[None] * n for _ in range(n)]
    for stud in range(0, n):
        for location in range(0, n):
            hosp = studentPreference[stud][location]
            rankStudent[stud][hosp] = location
    return rankStudent

# Checks For Blocking Pairs
def blockingPairCheck(n, HospStud, StudHosp, HospPrefer, studRank):
    # returns (stable, witness_string)
    for hosp in range(0, n):
        currentMatch = HospStud[hosp]
        for stud in HospPrefer[hosp]:
            if stud == currentMatch:
                break
            if studRank[stud][hosp] < studRank[stud][StudHosp[stud]]:
                outpString = "(" + str(hosp + 1) + ", " + str(stud + 1) + ")"
                return (False, outpString)

    return (True, "")

# Main
if __name__ == "__main__":
    if argc != 3:
        exit(1)
    preferencePath = argv[1]
    matchedPath = argv[2]

    # Edge Cases
    preferenceLines = readNonEmptyLines(preferencePath)
    if len(preferenceLines) == 0:
        print("Error: Preference File Is Empty")
        exit(0)
    try:
        n = to_int(preferenceLines[0])
    except:
        print("Error: First Line Isn't A Int")
        exit(0)

    if n <= 0:
        print("Error: n Isn't Positive")
        exit(0)

    expected = 1 + 2 * n
    if len(preferenceLines) != expected:
        print("Error: Supposed To Have " + str(expected) + " Lines, But Got " + str(len(preferenceLines)) + " Lines Instead")
        exit(0)

    # Parse Hospital Prefs
    hospPref = [None] * n
    for h in range(0, n):
        line = preferenceLines[1 + h]
        try:
            vals = intsFromLine(line)
        except:
            exit(0)

        if not validPermutation(vals, n):
            exit(0)

        hospPref[h] = [x - 1 for x in vals]

    # ---- Parse student prefs ----
    studPref = [None] * n
    for s in range(0, n):
        line = preferenceLines[1 + n + s]
        try:
            vals = intsFromLine(line)
        except:
            exit(0)

        if not validPermutation(vals, n):
            exit(0)

        studPref[s] = [x - 1 for x in vals]

    # ---- Read matching file ----
    matchingLine = readNonEmptyLines(matchedPath)
    if len(matchingLine) != n:
        exit(0)

    hospToStud = [-1] * n
    studToHosp = [-1] * n

    for line in matchingLine:
        try:
            pair = intsFromLine(line)
        except:
            exit(0)

        if len(pair) != 2:
            exit(0)

        i = pair[0]   
        j = pair[1]   
        h = i - 1
        s = j - 1

        if h < 0 or h >= n or s < 0 or s >= n:
            exit(0)

        if hospToStud[h] != -1:
            exit(0)

        if studToHosp[s] != -1:
            exit(0)

        hospToStud[h] = s
        studToHosp[s] = h

    # ---- Inline validity check (bijection + inverse) ----
    # Check all hospitals matched
    for h in range(0, n):
        if hospToStud[h] == -1:
            exit(0)

    # Check all students matched + inverse consistency
    for s in range(0, n):
        if studToHosp[s] == -1:
            exit(0)

    for h in range(0, n):
        s = hospToStud[h]
        if studToHosp[s] != h:
            exit(0)

    # Rank Table
    studRank = createRankingTable(n, studPref)

    # Check Stability
    stable, witness = blockingPairCheck(n, hospToStud, studToHosp, hospPref, studRank)