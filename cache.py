import datetime
def fib(n):
    fib_seq = [0, 1]
    for i in range(2, n):
        fib_seq.append(fib_seq[i - 2] + fib_seq[i - 1])
    return fib_seq[-1]


FIB_CACHE = {} # at module level, so it persists across function calls


def fib_with_cache(n):
    if n in FIB_CACHE:
        return FIB_CACHE[n]
    else:
        FIB_CACHE[n] = fib(n)
        return FIB_CACHE[n]



inp = input("What Fibonacci number would you like? ")
t1 = datetime.datetime.now().timestamp()
print(fib_with_cache(int(inp)))
t2 = datetime.datetime.now().timestamp()
inp = input("What Fibonacci number would you like? ")
t3 = datetime.datetime.now().timestamp()
print(fib_with_cache(int(inp)))
t4 = datetime.datetime.now().timestamp()
print("time without caching: ", (t2 - t1) * 1000, "ms")
print("time with caching: ", (t4 - t3) * 1000, "ms")