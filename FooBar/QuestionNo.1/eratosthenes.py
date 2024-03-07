def eratosthenes(num):
    vals = [i for i in range(2,num+1)]

    multiples = []
    primes = []
    primestring = ""

    for i in range(2, num, 1):
        if i not in multiples:
            p = i
            while i*p < num:
                mult = p*i 
                multiples.append(mult)
                p += 1

            primes.append(i)
            i = str(i)
            primestring = primestring + i
            print("LenStr:", len(primestring))
            print(primestring)

    return primestring

primestring = eratosthenes(20235)

def solution(n):
    id = primestring[n:n+5]
    return id

