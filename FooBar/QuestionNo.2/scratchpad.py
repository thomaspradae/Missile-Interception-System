# def solution(t, l):
list = [4, 3, 10, 2, 8, 12, 3, 4, 5, 2, 1, 5, 6, 3, 2, 4, 5, 23, 19]
i = 0
min = 0
target = 23
solution = []
list_length = len(list)

while i < list_length:

    if sum(solution) < target:
        solution.append(list[i])
        i += 1

    if sum(solution) > target:
        solution.pop(0)
        min += 1

    print(i)

    if sum(solution) == target:
        print(list[min:i]) 
        print(min, i)
        break




print("Solution Found")
print("Sum:", sum(solution))
# while i < list_length:



# target = 23 
# solution = []
# list_length = len(list)
# index = 0

# smallest_index = 
# largest_index

# # while sum(solution) != target:

# # while list_length > index: 

# #     if sum(solution) < target:
# #         solution.append(list[index])
# #         index += 1

# #     if sum(solution) > target:
# #         solution = solution[index + 1:]

#     # if sum(solution) == target:
#     # break

# print(sum(solution))



# print("Solution Found")

# list.pop()





# # while i < list_length:
# #     if sum(solution) < target:
# #         print("i:", i)
# #         print("Solution List Before:", solution)
# #         print("Solution Sum Before:", sum(solution))
# #         solution.append(list[i])
# #         print("Solution List After:", solution)
# #         print("Solution Sum Before:", sum(solution), "\n")
# #         i += 1

# #     else:
# #         print("BROKEN")
# #         break
        
