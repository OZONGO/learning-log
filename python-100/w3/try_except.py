# print("A")
# int("abc")
# print("B")

# try:
#     x = int("abc")
# except ValueError:
#     x = 0
# print(x)


# try:
#     d = {"a": 1}
#     print(d["b"])
# except ValueError:
#     print("数字不对")
# print("done")

# try:
#     d = {"a": 1}
#     print(d["b"])
# except KeyError:
#     print("数字不对")
# print("done")

try:
    d = {"a": 1}
    print(d["b"])
except Exception:
    pass
print("done")