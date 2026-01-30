import os
import random

def generateFiles():
    # References from https://www.geeksforgeeks.org/python/python-os-makedirs-method/

    # Creates directory to store input files in specific large sizes
    os.makedirs('data', exist_ok=True)
    testSizes = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]

    # Loops through each test size and creates corresponding input file
    for n in testSizes:
        fileName = f'data/input_{n}.txt'

        with open(fileName, 'w') as f:
            f.write(f"{n}\n")
            
            # Hospital Preferences
            for j in range (n):
                preferences = list(range(1, n + 1))
                random.shuffle(preferences)
                f.write(" ".join(map(str, preferences)) + "\n")

            # Student Preferences
            for j in range(n):
                preferences = list(range(1, n + 1))
                random.shuffle(preferences)
                f.write(" ".join(map(str, preferences)) + "\n")

        print("Created " + fileName)

def main():
    generateFiles()

if __name__ == "__main__":
    main()
