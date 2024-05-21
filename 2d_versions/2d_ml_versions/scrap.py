list = []
results = []

list.append(-10)
payments = [1, 0.9, 0.85, 0.75, 0.65, 0.55, 0.35, 0.25, 0.15, 0.05]

length = len(list)

for i in range(length):
    if list[i] > 0:
        if i < len(payments):
            results.append(list[i] * payments[i])
        else:
            results.append(list[i] * 0)
    else:
        results.append(list[i])
    

print("list", list)
print(results)

