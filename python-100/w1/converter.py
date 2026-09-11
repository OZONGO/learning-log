import numcheck
rate = 6.5  # 人民币兑换美元固定汇率,非实时汇率
while True:
    menu_choice = input(
        "请选择功能:\n"
        "1. 摄氏 → 华氏\n"
        "2. 华氏 → 摄氏\n"
        "3. 人民币 → 美元\n"
        "4. 美元 → 人民币\n"
        "q. 退出\n"
        "请输入选项: "
    )
    
    if menu_choice == 'q':
        break
    
    elif menu_choice == '1':
        while True:
            c = numcheck.num_check("摄氏温度")
            if c < -273.15:
                print("不能低于绝对零度")
                continue
            f = c * 9 / 5 + 32
            print(f"{c:.2f} 摄氏度 = {f:.2f} 华氏温度")
            break
    
    elif menu_choice == '2':
        while True:
            f = numcheck.num_check("华氏度")
            c = (f - 32) * 5 / 9
            if c < -273.15:
                print("不能低于绝对零度")
                continue  
            print(f"{f:.2f} 华氏度 = {c:.2f} 摄氏度")
            break
    
    elif menu_choice == '3':
        rmb = numcheck.num_check("人民币金额")
        usd = rmb / rate
        print(f"{rmb:.2f} 人民币 = {usd:.2f} 美元")
    
    elif menu_choice == '4':
        usd = numcheck.num_check("美元金额")
        rmb = usd * rate
        print(f"{usd:.2f} 美元 = {rmb:.2f} 人民币")
    
    else:
        print("请输入有效的选项")
        
