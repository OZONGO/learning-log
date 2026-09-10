"""
简易通讯录（单文件版）

设计取舍：
- 每次增/删/改后立刻 save_book 落盘，而不是退出时统一保存。
  代价是每次写盘都是一次不可逆截断（"w" 模式）；
  换来的是中途崩溃 / Ctrl-C 时数据不丢。
  正因为每次操作都已写盘，q 退出分支不需要再存一次。
- load_book 遇到损坏的 JSON，会先把原文另存为 *.brokenN，
  再以空通讯录启动。如果不做这一步，下一次 save_book 就会把
  原文彻底抹掉，"还能手工抢救出来的联系人"一个都不剩。

DoD（先写再动手）：
1. contacts.json 不存在 -> 不崩，从 {} 起步；添加后退出能生成文件。
2. 加两人 -> q -> 重开，两人还在。
3. 删一人 -> q -> 重开，确实少了；文件里对应记录也消失。
4. 改电话/邮箱 -> q -> 重开，改过的值还在。
5. 手动把 contacts.json 改成半截 -> 重开不崩，且原文被备份，
   不会被随后的 save_book 覆盖掉。
   json.load 抛的是 json.decoder.JSONDecodeError（ValueError 的子类），
   这里只捕它，不用 except ValueError 去吞 int(t) 的错误。
6. 中文在 json 文件里肉眼可读，因为 json.dump 用了 ensure_ascii=False。

约束：
- 自包含，不 import w1/ 或 w2/ 里的任何东西。
- 读写一律走 with，with 块里不再手写 f.close()。
- 每次 open 都写 encoding="utf-8"。
"""

import json

CONTACTS_FILE = "E:/AI/workspace/L/learning-log/python-100/w3/contacts.json"


def _backup_corrupt_file():
    with open(CONTACTS_FILE, "rb") as f:
        raw = f.read()
    n = 1
    while True:
        backup = f"{CONTACTS_FILE}.broken{n}"
        try:
            with open(backup, "xb") as f:
                f.write(raw)
            return backup
        except FileExistsError:
            n += 1


def load_book():
    try:
        with open(CONTACTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        backup = _backup_corrupt_file()
        print(f"contacts.json 格式损坏，原已备份到：{backup}")
        print("本次从空通讯录开始，请手工从备份里抢救数据。")
        return {}


def save_book(book):
    with open(CONTACTS_FILE, "w", encoding="utf-8") as f:
        json.dump(book, f, ensure_ascii=False, indent=4)


book = load_book()

while True:
    t = input("1-添加  2-删除  3-修改  4-查找  5-显示全部  q-退出\n")
    if t == "q":
        break

    try:
        choice = int(t)
    except ValueError:
        print("无效选项")
        continue

    if choice == 1:
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
        save_book(book)
    elif choice == 2:
        name = input("请输入姓名：")
        if name not in book:
            print("无此人")
            continue
        del book[name]
        save_book(book)
        print("删除成功")
    elif choice == 3:
        name = input("请输入姓名：")
        if name not in book:
            print("无此人")
            continue
        print(f"当前信息：电话-{book[name]['phone']}, 邮箱-{book[name]['email']}")
        while True:
            choice_sub = input("修改电话请输入1，修改邮箱请输入2：")
            if choice_sub == "1":
                new_phone = input("请输入新电话：")
                book[name]['phone'] = new_phone
                break
            elif choice_sub == "2":
                new_email = input("请输入新邮箱：")
                book[name]['email'] = new_email
                break
            else:
                print("无效选项")
                continue
        save_book(book)
    elif choice == 4:
        name = input("请输入姓名：")
        if name not in book:
            print("无此人")
            continue
        print(f"联系人信息：姓名-{name}, 电话-{book[name]['phone']}, 邮箱-{book[name]['email']}")
    elif choice == 5:
        if not book:
            print("通讯录为空")
        else:
            for name, info in book.items():
                print(f"姓名-{name}, 电话-{info['phone']}, 邮箱-{info['email']}")
    else:
        print("无效选项")

