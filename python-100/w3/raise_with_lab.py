# try:
#     def ra ():
#         raise ValueError("...")
#         print("会打吗")
#     ra()
# except ValueError as e:
#     print("接住：", e)
#预测:接住： ...


# def ra2 ():
#     raise ValueError("...")
#     print("会打吗")
# ra2()
#预测:ValueError: ...

# with open("E:/AI/workspace/L/learning-log/python-100/w3/notes_lab.txt","w",encoding="utf-8") as f:
#     f.write("a\n" )
#     f.write("b\n" )
#     f.close()
# with open("E:/AI/workspace/L/learning-log/python-100/w3/notes_lab.txt","w",encoding="utf-8") as f:
#     f.close()

# with open("E:/AI/workspace/L/learning-log/python-100/w3/notes_lab.txt","r",encoding="utf-8") as f:
#     text = f.read()
# print(text)

# with open("E:/AI/workspace/L/learning-log/python-100/w3/notes_lab.txt","w",encoding="utf-8") as f:
#     f.write("a\n" )
#     f.write("b\n" )
#     f.close()
# with open("E:/AI/workspace/L/learning-log/python-100/w3/notes_lab.txt","r",encoding="utf-8") as f:
#     print(f.read())
#     print(f.read())
#预测：a
#b
#
#

import json
l1 = {1: "a", "2": "b"}
with open("E:/AI/workspace/L/learning-log/python-100/w3/book_lab.json", "w", encoding="utf-8") as f:
    json.dump(l1, f, ensure_ascii=False, indent=2)
with open("E:/AI/workspace/L/learning-log/python-100/w3/book_lab.json", "r", encoding="utf-8") as f:
    data = json.load(f)
print(data[1])
# #预测:KeyError: 1    