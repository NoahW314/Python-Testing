import sys

line = sys.stdin.readline()
newLine = ""

for char in line:
    newLine += (char+" ")

print(newLine)