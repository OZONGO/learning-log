from collections import Counter
l1 = [1,2,3,4]
l2 = [x * x for x in l1]
l3 = []
for x in l1:
    l3.append(x * x)
print(l2)
print(l3)
print(l2 == l3)
l4 = ["a", "b", "a", "a", "c"]
print(f"{Counter(l4)}")
print(f"{Counter(l4).most_common(2)}")