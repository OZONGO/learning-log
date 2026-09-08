def show(*args, **kwargs):
    print(args)
    print(kwargs)

show (1,2,3)#(1,2,3)\n{}
show(name="李四", age=20)#() \n{'name': '李四', 'age': 20}
show(1, 2, name="any")#(1, 2)\n{'name': 'any'}
show(9, name="x", city="hz")#(9,)\n{'name': 'x', 'city': 'hz'}




def profile(name, age, **rest):
    print(name,age,rest)

# def total(*num):
#     return sum(num)
def total(a, b, c):
    return a + b + c
nums = [3, 1, 2]
d = {"name": "李四", "age": 20, "city": "杭州"}
profile(**d)#李四 20 {'city': '杭州'}
print(total(*nums))#6
print(total(*[1, 2])) #total() missing 1 required positional argument: 'c'
#profile(**{"name": "王五"})#profile() missing 1 required positional argument: 'age'