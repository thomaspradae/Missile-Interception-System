l = [4, 3, 10, 2, 8]
t = 12

i = 0
min = 0
solution = []
list_length = len(l)

print(l[2:3])
print("List Length:", list_length)

while i < list_length:
    print("Start i:", i)
    print("Start min:", min)
    print("Start List:", solution)
    print("Start Sum:", sum(solution))

    if sum(solution) < t:
        print("First Hole")
        solution.append(l[i])

        if sum(solution) == t:
            print(l[min:i])
            print(min, i)
            break

        i += 1

    else:
        print("Second Hole")
        solution.pop(0)
 
        if sum(solution) == t:
            print(l[min:i])
            print(min, i)
            break

        min += 1

    # if sum(solution) == t:
    #     print(l[min:i]) 
    #     print(min, i) 
    #     break 

    # elif sum(solution) < t:
    #     print("First Hole")
    #     solution.append(l[i])
    #     i += 1

    # else:
    #     print("Second Hole")
    #     solution.pop(0)
    #     min += 1

    print("End i:", i)
    print("End min:", min)
    print("End List:", solution)
    print("End Sum:", sum(solution), "\n")
       
print(-1, -1)


# l =  [4, 3, 10, 2, 8, 12, 3, 4, 5, 2, 1, 5, 6, 3, 2, 4, 5, 23, 19]
# t = 23


