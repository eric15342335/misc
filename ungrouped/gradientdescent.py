# eric15342335
def derivative(x: float) -> int:  # derivative of f(x) as given by the question
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0  # given


def learn(x: int) -> float:  # learning rate n
    return 1 / (x + 1)


def func(x: int) -> float:
    if x == 0:  # initial state x^(0)
        return 2.5
    elif x in grad:  # cache of x^(t)
        return grad[x]
    else:  # not in cache
        return func(x - 1) - learn(x - 1) * derivative(func(x - 1))


grad = {}
case = 99  # what value of t you want to calculate
for i in range(case + 1):
    grad[i] = func(i)  # store gradient descent value to cache
for i in range(case + 1):
    print(i, func(i))  # print value
