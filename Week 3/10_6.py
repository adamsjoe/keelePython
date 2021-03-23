# Write and test a Python function common that takes two lists and returns True if they have at least one common member and False otherwise.

def common(list1, list2):
    list1Set = set(list1)
    list2Set = set(list2)

    # if there exist one common element in the list1Set & list2Set returns a positive integer
    # otherwise it returns a 0
    if (list1Set & list2Set):
        return True
    else:
        return False

l1 = [1,2,3]
l2 = [1,2,3]
l3 = [3,4,5]
l4 = [7,8,9]

print(common(l1, l2)) #should be true - both match
print(common(l2, l3)) #should be true - 3 is common
print(common(l3, l4)) #should be false - no match
print(common(l1, l4)) #should be false - no match