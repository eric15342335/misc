import sys

def is_prime(n : int) -> bool:
    if n == 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, n//2+1, 2):
        if n % i == 0:
            return False
    return True

assert is_prime(2) == True
assert is_prime(3) == True
assert is_prime(5) == True
assert is_prime(7) == True
assert is_prime(11) == True

if len(sys.argv) > 1:
    print(is_prime(int(sys.argv[1])))

print(list(filter(is_prime, [i for i in range(2,100)])))
