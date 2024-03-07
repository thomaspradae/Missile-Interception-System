def solution(l, t):
    i = 0
    min = 0
    max = 0
    iter = 0
    solution = []
    list_length = len(l)

    while i < list_length:
        print("Start iter:", iter)
        print("Start i:", i)
        print("Start min:", min)
        print("Start max:", max)        
        print("Start Sum:", sum(solution), "\n")
        print("Start List:", solution)

        if sum(solution) < t:
            solution.append(l[i])
            print("TEMPORAL", max)
            max += 1
            print("SECOND", max)

            if sum(solution) == t:
                print(solution)
                return min, i
            
            i += 1

        else:
            solution.pop(0)

            if sum(solution) == t:
                iter += 1
                print(solution)
                return min, i

            min += 1

        if sum(solution) != t: 
            iter += 1

        print("End iter:", iter)
        print("End i:", i)
        print("End min:", min)
        print("End max:", max)
        print("End Sum:", sum(solution), "\n")
        print("End List:", solution)
        print("\n")
        print("---------")
        print("\n")

    return -1, -1
        

l = [4, 3, 10, 2, 8, 12, 3, 4, 5, 2, 1, 5, 6, 3, 2, 4, 5, 23, 19]
t = 25

print(solution(l, t))



        # if sum(solution) > t:
        #     solution.pop(0)
        #     min += 1

        # elif sum(solution) == t:
        #     print(l[min:i+1])
        #     return min, i
        
        # solution.append(l[i])
        # i += 1

        # print(solution)
        # print(sum(solution), "\n")