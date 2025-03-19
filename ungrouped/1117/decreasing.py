current = int(input())
decreased_count = 0
for _ in range(9):
    previous = current
    current = int(input())
    if previous > current:
        decreased_count += 1

print(decreased_count)
