#01
x = 10

def f():
    x = 5

f()
print(x)#10

#02
nums = [1, 2, 3]
def f2():
    nums.append(4)
f2()
print(nums)#[1, 2, 3, 4]

#03
x3 = 10
def f3():
    print(  x3)
    x3 = 5
f3()
print(x3)#10

#04
x4 = 10
def f4():
    global x4
    print(x4)
    x4 = 5
f4()
print(x4)#5