# Write a function called nested_sum that takes a list of lists of integers and adds up the elements from all of the nested lists. For example:

# t = [[1, 2], [3], [4, 5, 6]]
# print(nested_sum(t))

# 21

def nested_sum(theBigList):
    total = 0

    for number in theBigList:
        if type(number) == int:
            # print("int found")
            total += number
        elif type(number) == list:
            # print("list found")
            for nestedNum in number:
                total += nestedNum
    return total

t=[1,2,3,[4,5]]
print("total is", nested_sum(t))
