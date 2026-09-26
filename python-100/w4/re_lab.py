#re_lab.py


import re


def sep(title):
    print("\n" + "=" * 10, title, "=" * 10)


# ============================================================
# 实验1：课例复现
# 预测：
# findall -> ['2026-09-26', '2026-10-15']
# search 带组 -> group(0)='2026-09-26', group(1)='2026',
#                group(2)='09', group(3)='26',
#                groups()=('2026','09','26')
# ============================================================
sep("实验1 课例复现")
text1 = "截止 2026-09-26 交，延期到 2026-10-15 也行。"

hits1 = re.findall(r"\d{4}-\d{2}-\d{2}", text1)
print("findall:", hits1)

m1 = re.search(r"(\d{4})-(\d{2})-(\d{2})", text1)
print("search group(0):", m1.group(0))
print("search group(1):", m1.group(1))
print("search group(2):", m1.group(2))
print("search group(3):", m1.group(3))
print("search groups():", m1.groups())


# ============================================================
# 实验2：量词家族
# 预测：
# ? -> ['color', 'colour']
# * -> ['color', 'colour', 'colouur', 'colouuur', 'colouuuur']
# + -> ['colour', 'colouur', 'colouuur', 'colouuuur']
# {2,3} -> ['colouur', 'colouuur']
# ============================================================
sep("实验2 量词家族")
text2 = "color colour colouur colouuur colouuuur"
print("?     :", re.findall(r"colou?r", text2))
print("*     :", re.findall(r"colou*r", text2))
print("+     :", re.findall(r"colou+r", text2))
print("{2,3} :", re.findall(r"colou{2,3}r", text2))


# ============================================================
# 实验3：字符类
# 预测：
# [abc] -> ['a', 'b', 'c']
# [a-z] -> ['a', 'c']
# [^abc] -> ['d', 'e']
# . 默认 -> ['a', 'b']，换行符 \n 不吃
# . DOTALL -> ['a', '\n', 'b']
# ============================================================
sep("实验3 字符类")
print("[abc]     :", re.findall(r"[abc]", "abcde"))
print("[a-z]     :", re.findall(r"[a-z]", "aBc123"))
print("[^abc]    :", re.findall(r"[^abc]", "abcde"))
print(". 默认    :", re.findall(r".", "a\nb"))
print(". DOTALL  :", re.findall(r".", "a\nb", re.DOTALL))


# ============================================================
# 实验4：锚点
# 预测：
# \bcat\b 英文靶 -> ['cat', 'cat']
# ^\w+ 默认 -> ['abc']
# ^\w+ re.M -> ['abc', 'def']
# \d+$ 默认 -> ['456']
# \d+$ re.M -> ['123', '456']
# \bcat\b 中文靶 -> ['cat']，中文夹着的 cat 不匹配
# ============================================================
sep("实验4 锚点")
text4 = "cat category catalog a cat"
print(r"\bcat\b        :", re.findall(r"\bcat\b", text4))
print(r"^\w+ 默认      :", re.findall(r"^\w+", "abc\ndef"))
print(r"^\w+ re.M      :", re.findall(r"^\w+", "abc\ndef", re.M))
print(r"\d+$ 默认      :", re.findall(r"\d+$", "abc 123\ndef 456"))
print(r"\d+$ re.M      :", re.findall(r"\d+$", "abc 123\ndef 456", re.M))
print(r"\bcat\b 中文靶 :", re.findall(r"\bcat\b", "猫cat狗 cat 猫"))


# ============================================================
# 实验5：常见错误复现
# 预测：
# ① re.compile("*.py") -> re.error: nothing to repeat at position 0
# ② a.py -> ['a.py', 'aXpy', 'aapy', 'a/py']
#    a\.py -> ['a.py']
# ③ match -> None；search -> '2026'
# ============================================================
sep("实验5 常见错误复现")

try:
    re.compile("*.py")
except re.error as e:
    print("re.compile('*.py') 报错:", e)

text5 = "a.py aXpy aapy a/py"
print(r"a.py  :", re.findall(r"a.py", text5))
print(r"a\.py :", re.findall(r"a\.py", text5))

m5_match = re.match(r"\d{4}", "abc 2026")
m5_search = re.search(r"\d{4}", "abc 2026")
print("match :", m5_match)
print("search:", m5_search.group(0) if m5_search else None)


# ============================================================
# 实验6：贪心发现题
# 预测（先写，翻车不许改）：
# 我猜 ['a', 'b']。但知道 + 默认贪心，可能实际翻车为 ['a><b']。
# ============================================================
sep("实验6 贪心发现题")
text6 = "<a><b>"
print("findall :", re.findall(r"<(.+)>", text6))
print("非贪婪  :", re.findall(r"<(.+?)>", text6))
print("排除 >  :", re.findall(r"<([^>]+)>", text6))


# ============================================================
# 实验7：综合小任务
# 预测：
# 日期 -> ['2026-09-26', '2026-10-15', '2026-11-01']
# 周次 -> ['W3', 'W4', 'W12', 'W3', 'W3']
# py文件 -> ['report.py', 'main.py', 'utils.py', 'app.py']
# ============================================================
sep("实验7 综合小任务")
text7 = """第 W3 周：2026-09-26 交 report.py，备注见 notes.txt。
W4 补交 main.py 和 utils.py，日期 2026-10-15。
W12 最终版：app.py 截止 2026-11-01。
普通句子 W3 不是周次吗？W3 是周次标记。
"""

print("日期   :", re.findall(r"\d{4}-\d{2}-\d{2}", text7))
print("周次   :", re.findall(r"\bW\d+\b", text7))
print("py文件 :", re.findall(r"\b[\w.-]+\.py\b", text7))