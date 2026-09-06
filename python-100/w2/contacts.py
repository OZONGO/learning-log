'''
数据：程序运行期间维护一个通讯录，每条联系人含姓名、电话、邮箱。姓名是识别一条联系人的唯一依据（所以不允许改名）。

菜单循环：启动后循环显示菜单，等用户选：
1-添加  2-删除  3-修改  4-查找  5-显示全部  q-退出
| 操作 | 行为 | 边界规则 |
| --- | --- | --- |
| 1 添加 | 依次输入姓名、电话、邮箱 | 姓名为空 → 拒绝并提示；姓名已存在 → 拒绝（“已存在”，不许覆盖旧数据）；电话/邮箱可为空 |
| 2 删除 | 输入姓名 | 不存在 → 提示“无此人”；存在 → 删除并确认 |
| 3 修改 | 输入姓名 → 先显示此人当前电话/邮箱 → 问改哪个（1-电话 2-邮箱）→ 输入新值 | 不存在 → 提示“无此人”；姓名不可改 |
| 4 查找 | 输入姓名，打印此人完整信息 | 不存在 → 提示“无此人” |
| 5 显示全部 | 逐行打印每条联系人（格式自定，姓名/电话/邮箱能看清即可） | 空通讯录 → 提示“通讯录为空” |
| q 退出 | 干净结束，无报错 | — |

通用规则：

菜单输入 1/2/3/4/q 之外的任何东西（空回车、乱敲字符）→ 打印“无效选项”，重显菜单，绝不崩溃
全程零崩溃是硬要求，任何输入都不能让程序 traceback
'''
book = {}
while True:
    t = input("1-添加  2-删除  3-修改  4-查找  5-显示全部  q-退出\n")
    if t == "q":
        break
    elif t in ("1", "2", "3", "4", "5"):
        if t == "1":
            name = input("请输入姓名：")
            if name == "":
                print("姓名不能为空")
                continue
            if name in book:
                print("已存在")
                continue
            phone = input("请输入电话：")
            email = input("请输入邮箱：")
            book[name] = {"phone": phone, "email": email}
        elif t == "2":
            name = input("请输入姓名：")
            if name not in book:
                print("无此人")
                continue
            del book[name]
            print("删除成功")
        elif t == "3":  
            name = input("请输入姓名：")
            if name not in book:
                print("无此人")
                continue
            print(f"当前信息：电话-{book[name]['phone']}, 邮箱-{book[name]['email']}")
            while True:
                choice = input("修改电话请输入1，修改邮箱请输入2：")
                if choice == "1":
                    new_phone = input("请输入新电话：")
                    book[name]['phone'] = new_phone
                    break
                elif choice == "2":
                    new_email = input("请输入新邮箱：")
                    book[name]['email'] = new_email
                    break
                else:
                    print("无效选项")
                    continue
        elif t == "4":
            name = input("请输入姓名：")
            if name not in book:
                print("无此人")
                continue
            print(f"联系人信息：姓名-{name}, 电话-{book[name]['phone']}, 邮箱-{book[name]['email']}")
        elif t == "5":
            if not book:
                print("通讯录为空")
            else:
                for name, info in book.items():
                    print(f"姓名-{name}, 电话-{info['phone']}, 邮箱-{info['email']}")

    else:
        print("无效选项")
        continue
