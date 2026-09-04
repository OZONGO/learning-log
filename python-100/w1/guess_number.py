import random
answer = random.randint(1, 100)
while True:
    guess = int(input("请输入一个数字："))
    if answer > guess:
        print("猜小了")
    elif answer < guess:
        print("猜大了")
    else:
        print("猜对了")
        break