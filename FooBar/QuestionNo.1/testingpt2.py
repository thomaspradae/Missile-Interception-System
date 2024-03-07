def primePro():
    primes = [2]
    primeString = "2"
    
    currentNum = 3
    while len(primeString) < 10009:
        isPrime = True
        i = 0 
        while i < len(primes) and isPrime:
            if currentNum % primes[i] == 0:
                isPrime = False
            i+=1

        if isPrime:
            primes.append(currentNum)
            primeString += str(currentNum)
        
        currentNum+=1
    
    return primeString

def solution(n):
    primeString = primePro()
    id = primeString[n:n+5]
    return id

print(solution(3))