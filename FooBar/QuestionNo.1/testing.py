import timeit
# from memory_profiler import profile

# @profile
def eratosthenes(num):
    vals = [i for i in range(2, num + 1)]

    multiples = []
    primes = []
    primestring = ""

    for i in range(2, num, 1):
        if i not in multiples:
            p = i
            while i * p < num:
                mult = p * i
                multiples.append(mult)
                p += 1

            primes.append(i)
            i = str(i)
            primestring = primestring + i
            print("LenStr:", len(primestring))
            print(primestring)

    return primestring


primestring = eratosthenes(20235)

# @profile
def solution(n):
    id = primestring[n:n + 5]
    return id

# Measure execution time
execution_time = timeit.timeit("eratosthenes(20235)", globals=globals(), number=1)
print(f"Execution time: {execution_time:.6f} seconds")

# # Measure memory usage
# mem_usage = memory_profiler.memory_usage((eratosthenes, (20235,), {}))
# print(f"Peak memory usage: {max(mem_usage)} MiB")

# # Test solution function
# result = solution(123)
# print("Result:", result)
