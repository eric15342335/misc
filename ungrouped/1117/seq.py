def f(a:int)->int:
    if a == 0:
        return 2
    if a == 1:
        return 1
    if a == 2:
        return 3
    return f(a-2)*f(a-3)

print(f(15))