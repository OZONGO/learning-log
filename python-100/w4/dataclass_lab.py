# dataclass_lab.py
# W4 预习第三块：dataclass（2026-09-17）

# ============================================================
# 实验1：对比——手写 vs @dataclass
# ============================================================
# 【预测先行】
# 下面两段代码，效果完全一样。
# A 段（手写）：逐行预测每一行输出
# B 段（dataclass）：逐行预测每一行输出
# 然后回答：B 段比 A 段少写了几行代码？少了哪些方法？

# --- A 段：手写 ---
class PointManual:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"PointManual(x={self.x}, y={self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


# --- B 段：dataclass ---
from dataclasses import dataclass

@dataclass
class PointDC:
    x: int
    y: int


print("=== 实验1：手写 vs dataclass ===")
p1 = PointManual(3, 4)
p2 = PointManual(3, 4)
print("A: p1 =", p1)
print("A: p1 == p2 =", p1 == p2)

p3 = PointDC(3, 4)
p4 = PointDC(3, 4)
print("B: p3 =", p3)
print("B: p3 == p4 =", p3 == p4)

# 【对账】
# A: p1 = PointManual(x=3, y=4)
# A: p1 == p2 = True
# B: p3 = PointDC(x=3, y=4)
# B: p3 == p4 = True
# 两段输出格式几乎一样（只是类名不同）。
# B 段少了 __init__ / __repr__ / __eq__ 三段，共约 7 行。


# ============================================================
# 实验2：可变默认值陷阱
# ============================================================
# 【预测先行】
# 以下代码创建两个 Bad 实例，往 b1.tags 里 append "bug"。
# 预测：b2.tags 会是什么？是 [] 还是 ["bug"]？
#
# class Bad:
#     def __init__(self, tags=[]):
#         self.tags = tags
#
# b1 = Bad()
# b1.tags.append("bug")
# b2 = Bad()
# print(b2.tags)   # ???

print("\n=== 实验2：可变默认值陷阱 ===")

class Bad:
    def __init__(self, tags=[]):
        self.tags = tags

b1 = Bad()
b1.tags.append("bug")
b2 = Bad()
print("b2.tags =", b2.tags)

# 【对账】
# b2.tags = ['bug']
# 原因：tags=[] 只在 def 时求值一次，两个实例共享同一个 list。
# 这和你之前学的"函数默认值陷阱"（N007）是同一个坑——
# 默认参数在 def 时定死，不是每次调用时新建。


# ============================================================
# 实验3：field(default_factory=...) 修复
# ============================================================
# 【预测先行】
# 用 dataclass + field(default_factory=list) 重写上面的 Bad。
# 预测：b3 和 b4 的 tags 是否共享？
#
# from dataclasses import dataclass, field
#
# @dataclass
# class Good:
#     tags: list = field(default_factory=list)
#
# g1 = Good()
# g1.tags.append("ok")
# g2 = Good()
# print(g2.tags)   # ???

print("\n=== 实验3：field(default_factory=list) ===")

from dataclasses import dataclass, field

@dataclass
class Good:
    tags: list = field(default_factory=list)

g1 = Good()
g1.tags.append("ok")
g2 = Good()
print("g2.tags =", g2.tags)

# 【对账】
# g2.tags = []
# field(default_factory=list) 让每次创建实例时都新建一个 []，
# 不再共享。与 Bad 的区别就是"创建时求值 vs 每次调用时求值"。


# ============================================================
# 实验4：__post_init__ 做校验
# ============================================================
# 【预测先行】
# 以下代码尝试 CircleDC(-5) 和 CircleDC(3)，各会发生什么？
#
# @dataclass
# class CircleDC:
#     r: float
#
#     def __post_init__(self):
#         if self.r < 0:
#             raise ValueError("半径不能为负")
#
# print(CircleDC(-5))   # ???
# print(CircleDC(3))    # ???

print("\n=== 实验4：__post_init__ 校验 ===")

@dataclass
class CircleDC:
    r: float

    def __post_init__(self):
        if self.r < 0:
            raise ValueError("半径不能为负")

try:
    print("CircleDC(-5) =", CircleDC(-5))
except Exception as e:
    print(f"CircleDC(-5) → {type(e).__name__}: {e}")

print("CircleDC(3) =", CircleDC(3))

# 【对账】
# CircleDC(-5) → ValueError: 半径不能为负
# CircleDC(3) = CircleDC(r=3)
# __post_init__ 在自动生成的 __init__ 之后自动执行，
# 等价于你之前写的 __init__ + setter 校验，但写法更简洁。
# 注意：CircleDC(3) 的 r 显示为 3（int），不是 3.0（float）——
# 类型提示 float 不做运行时转换，传什么存什么（类型提示≠强制转换）。


# ============================================================
# 实验5：dataclass + @property 能混用吗？
# ============================================================
# 【预测先行】
# 以下代码尝试 PointProp(3, 4) 并访问 .dist。
# 预测：.dist 的值是多少？
#
# @dataclass
# class PointProp:
#     x: int
#     y: int
#
#     @property
#     def dist(self):
#         return (self.x ** 2 + self.y ** 2) ** 0.5
#
# p = PointProp(3, 4)
# print(p.dist)   # ???

print("\n=== 实验5：dataclass + @property ===")

import math

@dataclass
class PointProp:
    x: int
    y: int

    @property
    def dist(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

p = PointProp(3, 4)
print("p.dist =", p.dist)

# 【对账】
# p.dist = 5.0
# dataclass 和 @property 可以混用。
# @property 不参与 __init__ 的生成（因为它不是字段声明），
# 所以 dist 不会出现在构造函数的参数里——它是"派生量"，不是"存储量"。
# 这和你之前学的 Circle（r 存、area 算）是同一个思路。
