rate = 6.5  # 人民币兑换美元固定汇率,非实时汇率
while True:
    menu_choice = input("请选择功能：1. 摄氏 → 华氏\n2. 华氏 → 摄氏\n3. 人民币 → 美元\n4. 美元 → 人民币\nq. 退出\n请输入选项：")
    if menu_choice == 'q':
        break

    elif menu_choice == '1':
        while True:
            in_c = input("请输入摄氏温度：")
            # 验证输入是否为有效数字（允许负数和小数）
            if in_c.count("-") > 1 or in_c.count(".") > 1:
                print("请输入有效的摄氏温度")
            else:
                # 去掉一个负号和一个点后检查剩余字符是否为数字
                checked = in_c.replace(".", "", 1).replace("-", "", 1)
                if not checked.isdigit():
                    print("请输入有效的摄氏温度")
                    continue
                elif in_c.count("-") == 1 and not in_c.startswith("-"):
                    print("请输入有效的摄氏温度")
                    continue
                else:
                    c_val = float(in_c)
                    if c_val < -273.15:
                        print("摄氏温度不能低于绝对零度")
                        continue
                    else:
                        out_f = c_val * 9 / 5 + 32
                        print(f"{c_val:.2f} 摄氏度 = {out_f:.2f} 华氏度")
                        break

    elif menu_choice == '2':
        while True:
            in_f = input("请输入华氏温度：")
            if in_f.count("-") > 1 or in_f.count(".") > 1:
                print("请输入有效的华氏温度")
                continue
            else:
                checked = in_f.replace(".", "", 1).replace("-", "", 1)
                if not checked.isdigit():
                    print("请输入有效的华氏温度")
                    continue
                elif in_f.count("-") == 1 and not in_f.startswith("-"):
                    print("请输入有效的华氏温度")
                    continue
                else:
                    f_val = float(in_f)
                    c_val = (f_val - 32) * 5 / 9
                    if c_val < -273.15:
                        print("华氏温度不能低于绝对零度")
                        continue
                    else:
                        print(f"{f_val:.2f} 华氏度 = {c_val:.2f} 摄氏度")
                        break

    elif menu_choice == '3':
        while True:
            rmb = input("请输入人民币金额：")
            if rmb.count("-") > 1 or rmb.count(".") > 1:
                print("请输入有效的人民币金额")
                continue
            else:
                checked = rmb.replace(".", "", 1).replace("-", "", 1)
                if not checked.isdigit():
                    print("请输入有效的人民币金额")
                    continue
                elif rmb.count("-") == 1 and not rmb.startswith("-"):
                    print("请输入有效的人民币金额")
                    continue
                else:
                    rmb_val = float(rmb)
                    usd = rmb_val / rate
                    print(f"{rmb_val:.2f} 人民币 = {usd:.2f} 美元")
                    break
    elif menu_choice == '4':
        while True:
            usd = input("请输入美元金额：")
            if usd.count("-") > 1 or usd.count(".") > 1:
                print("请输入有效的美元金额")
                continue
            else:
                checked = usd.replace(".", "", 1).replace("-", "", 1)
                if not checked.isdigit():
                    print("请输入有效的美元金额")
                    continue
                elif usd.count("-") == 1 and not usd.startswith("-"):
                    print("请输入有效的美元金额")
                    continue
                else:
                    usd_val = float(usd)
                    rmb = usd_val * rate
                    print(f"{usd_val:.2f} 美元 = {rmb:.2f} 人民币")
                    break
    else:
        print("请输入有效的选项")