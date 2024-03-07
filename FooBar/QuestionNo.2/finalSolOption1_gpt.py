def solution(l, t):
    min = 0
    i = 0
    current_sum = 0

    while i < len(l):
        print("Start i:", i)
        print("Start Sum:", current_sum)
        current_sum += l[i]

        while current_sum > t:
            print("Inside Hole")
            current_sum -= l[min]
            min += 1

        if current_sum == t:
            print(l[min:i+1])
            return min, i
        
        print("Final i:", i)
        print("Final Min:", min, "\n")

        i += 1

    return -1, -1

# Example usage:
l = [4, 3, 10, 2, 8, 12, 3, 4, 5, 2, 1, 5, 6, 3, 2, 4, 5, 23, 19]
t = 25
print(solution(l, t))
