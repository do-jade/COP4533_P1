with open('tests/input.txt', 'r') as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

# n = number of hospitals/students
n = int(lines[0])

hospitalPreferences = []
studentPreferences = []

for i in range(1, n + 1):
    preferences = list(map(int, lines[i].split()))
    hospitalPreferences.append(preferences)

for i in range(n + 1, 2 * n + 1):
    preferences = list(map(int, lines[i].split()))
    studentPreferences.append(preferences)

