def solution(l, t):
    i = 0
    min = 0
    solution = []
    list_length = len(l)

    while i < list_length:
        
        if sum(solution) < t:
            solution.append(l[i])
            i += 1

        if sum(solution) > t:
            solution.pop(min)
            min += 1

        if sum(solution) == t:
            print(l[min:i]) 
            return min, i
    
    return -1, -1


# l =  [4, 3, 10, 2, 8, 12, 3, 4, 5, 2, 1, 5, 6, 3, 2, 4, 5, 23, 19]
# t = 23

l = [4, 3, 10, 2, 8]
t = 12

print(solution(l, t))