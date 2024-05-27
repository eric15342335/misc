fileObject = open("numberlist.txt")
L = fileObject.read().splitlines()
fileObject.close()

print(L)
L = list(map(int, L))
print(L)

numOccurMajority = len(L) // 2
countOccur = dict()
for numbers in L:
    countOccur[numbers] = countOccur.get(numbers, 0) + 1
for key in countOccur:
    if countOccur[key] > numOccurMajority:
        print("Yes")
        break
else:
    print("No")
