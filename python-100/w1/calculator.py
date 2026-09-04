while True:
    operation = input("请输入运算符（+、-、*、/）或输入 'q' 退出：")
    if operation == 'q':
        break
    if operation not in ['+', '-', '*', '/']:
        print("无效的运算符，请重新输入")
        continue
    else:
        while True:
            num1 = (input("请输入第一个数字："))
            num2 = (input("请输入第二个数字："))
            if num1.isdigit() and num2.isdigit():
                num1 = float(num1)
                num2 = float(num2)
                if operation == '+':
                    result = num1 + num2
                    print(f"结果是：{result}")
                    break
                elif operation == '-':
                    result = num1 - num2
                    print(f"结果是：{result}")
                    break
                elif operation == '*':
                    result = num1 * num2
                    print(f"结果是：{result}")
                    break
                elif operation == '/':
                    if num2 != 0:
                        result = num1 / num2
                        print(f"结果是：{result}")
                        break
                    else:
                        print("除数不能为零")
                        continue
            else:
                print("请输入有效的数字")
                continue

    
