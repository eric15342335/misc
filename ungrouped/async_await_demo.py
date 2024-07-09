import timeit

complexity = 1000

async def do_stuff_sync():
    for i in range(complexity):
        print(i)

async def stuff_sync():
    await do_stuff_sync()
    await do_stuff_sync()

# This message is printed before the do_stuff_sync() is called
print("perf (async/await)=", timeit.timeit(stuff_sync, number=1))

def do_stuff():
    for i in range(complexity):
        print(i)

def stuff():
    do_stuff()
    do_stuff()

print("perf (traditional)=", timeit.timeit(stuff, number=1))
