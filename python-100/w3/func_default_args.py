# def add_item(item, lst=[]):
#     lst.append(item)
#     return lst

# print(add_item("a"))
# print(add_item("b"))
# print(add_item.__defaults__)   # 此刻已经跑过上面两次调用


def add_item(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst

print(add_item("a")) #['a']
print(add_item("b")) #['b']

my_list = [1, 2, 3]
add_item("x", my_list)
print(my_list)