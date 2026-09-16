#inherit_lab.py


import os

MODE = os.environ.get("MODE", "1")


def section(title):
    print("\n" + "=" * 64)
    print(title)
    print("=" * 64)


#实验1  
# a. Dog("旺柴").speak() → 走 Animal.speak（Dog 没写），打出 "旺柴 发出声音"。
#     name 是 Dog 实例通过继承来的 Animal.__init__ 存的。
# b. Cat("咪").speak() → Cat.speak 赢，返回 "咪 喵喵叫"。
#     Animal.speak 没被删，还在 Animal 上，只是 Cat 的 MRO 在 Cat 这层就截胡。
# c. Animal("普通动物").speak() → 父类版还在："普通动物 发出声音"。
#     证伪"覆盖＝删除"。
# d. Dog.speak 是函数对象，显示 <function Animal.speak at ...>——
#    因为 speak 的方法体只定义在 Animal，Dog 没重写，只是继承拿到。
#    Dog("旺柴").speak 是绑定方法，显示 <bound method Animal.speak of <Dog instance>>。
#    两者都显示 Animal.speak（函数定义处），但后者 self 已绑到 Dog 实例。
#    "方法体谁提供"和"self 绑到谁"是两件事：前者看定义处，后者看访问方式。
# e. Dog.__mro__ = (Dog, Animal, object)，与口述"子→父→object"一致。


class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} 发出声音"


class Dog(Animal):
    def fetch(self):
        return f"{self.name} 在捡球"


class Cat(Animal):
    def speak(self):
        return f"{self.name} 喵喵叫"


print("a. Dog('旺柴').speak()       =", Dog("旺柴").speak())
print("b. Cat('咪').speak()         =", Cat("咪").speak())
print("c. Animal('普通动物').speak() =", Animal("普通动物").speak())
print("d. Dog.speak                 =", Dog.speak)
print("   Dog('旺柴').speak          =", Dog("旺柴").speak)
print("e. Dog.__mro__               =", Dog.__mro__)

# 【对账】
# a. 命中：走 Animal.speak，返回 "旺柴 发出声音"。
# b. 命中：Cat.speak 赢，返回 "咪 喵喵叫"。父类版仍在（见 c）。
# c. 命中："普通动物 发出声音"，覆盖≠删除。
# d. 命中：Dog.speak = <function Animal.speak at ...>；
#           Dog('旺柴').speak = <bound method Animal.speak of ...>
#           ——注意绑定方法显示的是 Animal.speak（方法本体定义在 Animal），
#           但绑定对象是 Dog 实例，继承下绑定机制照旧。
# e. 命中：(Dog, Animal, object)。


#实验2
# a. ChildNoSuper(1,2).a → AttributeError:
#    "'ChildNoSuper' object has no attribute 'a'"
# b. ChildNoSuper(1,2).b → 正常，返回 2。
# c. ChildSuper(1,2).a → 正常，返回 1（super().__init__(a) 跑过了）。
# d. ChildNoSuper(1,2).describe() → 构造时不炸，方法体内读 self.a 时炸
#    AttributeError: 'ChildNoSuper' object has no attribute 'a'。
#    坏数据藏到下游才炸。


class Base:
    def __init__(self, a):
        self.a = a

    def describe(self):
        return self.a


class ChildNoSuper(Base):
    def __init__(self, a, b):
        self.b = b


class ChildSuper(Base):
    def __init__(self, a, b):
        super().__init__(a)
        self.b = b


try:
    print("a. ChildNoSuper(1,2).a =", ChildNoSuper(1, 2).a)
except Exception as e:
    print(f"a. {type(e).__name__}: {e}")

print("b. ChildNoSuper(1,2).b =", ChildNoSuper(1, 2).b)
print("c. ChildSuper(1,2).a   =", ChildSuper(1, 2).a)

try:
    print("d. ChildNoSuper(1,2).describe() =", ChildNoSuper(1, 2).describe())
except Exception as e:
    print(f"d. {type(e).__name__}: {e}")

# 【对账】
# a. 命中：AttributeError: 'ChildNoSuper' object has no attribute 'a'
# b. 命中：2
# c. 命中：1
# d. 命中：构造没炸，调 describe() 时在方法体内读 self.a 才炸：
#    AttributeError: 'ChildNoSuper' object has no attribute 'a'


#实验3
# 【预测先行·态1（两个都有）】
#   print(p)      → 走 __str__ → "(3, 4)"
#   print([p])    → 列表内部对元素用 __repr__ → "[Point(3, 4)]"
#   print(repr(p))→ 走 __repr__ → "Point(3, 4)"
# 【预测先行·态2（屏蔽 __str__）】
#   print(p)      → __str__ 没了，回退到 __repr__ → "Point(3, 4)"
#   print([p])    → 不变，仍走 __repr__ → "[Point(3, 4)]"
#   print(repr(p))→ 不变 → "Point(3, 4)"
#   只有 print(p) 那一行变。
# 【预测先行·态3（两个都屏蔽）】
#   三者都回退到 object.__repr__ → "<__main__.Point object at 0x...>"
# 【预测先行·加餐 MODE=4（只写 __repr__）】
#   print(p) → 回退到 __repr__ → "Point(3, 4)"
#   —— 专打"回退单向"：str→repr 有路，repr→str 没路。


if MODE == "1":
    class Point:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def __repr__(self):
            return f"Point({self.x}, {self.y})"

        def __str__(self):
            return f"({self.x}, {self.y})"

elif MODE == "2":
    # 只用逐行 # 屏蔽 __str__（三引号是字符串表达式语句，会假屏蔽）
    class Point:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def __repr__(self):
            return f"Point({self.x}, {self.y})"

        # def __str__(self):
        #     return f"({self.x}, {self.y})"

elif MODE == "3":
    # __str__ 和 __repr__ 都 # 掉
    class Point:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        # def __repr__(self):
        #     return f"Point({self.x}, {self.y})"

        # def __str__(self):
        #     return f"({self.x}, {self.y})"

elif MODE == "4":
    # 加餐：只写 __repr__，不写 __str__
    class Point:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def __repr__(self):
            return f"Point({self.x}, {self.y})"

else:
    raise SystemExit(f"未知 MODE={MODE}")

p = Point(3, 4)
print("print(p)       =", p)
print("print([p])     =", [p])
print("print(repr(p)) =", repr(p))

# 【对账】
# 态1（MODE=1）：
#   print(p)       = (3, 4)           → 走 __str__ ✅
#   print([p])     = [Point(3, 4)]    → 列表对元素用 __repr__ ✅
#   print(repr(p)) = Point(3, 4)      → 走 __repr__ ✅
# 态2（MODE=2）：
#   print(p)       = Point(3, 4)      → __str__ 没了，回退 __repr__ ✅（变了）
#   print([p])     = [Point(3, 4)]    → 不变 ✅
#   print(repr(p)) = Point(3, 4)      → 不变 ✅
#   只有第一行变，与预测一致。
# 态3（MODE=3）：
#   print(p)       = <__main__.Point object at 0x...>       ✅
#   print([p])     = [<__main__.Point object at 0x...>]     ✅
#   print(repr(p)) = <__main__.Point object at 0x...>       ✅
#   全部回退到 object.__repr__ 的默认格式。
# 加餐（MODE=4）：
#   print(p) = Point(3, 4) → 只写 __repr__ 时，print 也会拿到 __repr__。
#   回退单向确认：str→repr 有路，repr→str 没路（态2 里 [p]、repr(p)
#   并没有跑去用 __str__）。


#实验4
# 【预测先行·无 setter 的 area】
# a. c.area       → 12.56636（π 用 3.14159，2**2=4，3.14159*4=12.56636）
# b. c.area()     → TypeError: 'float' object is not callable
#    （c.area 先算出 float，float 不可调用）
# c. c.area = 99  → AttributeError: property 'area' of 'Circle'
#                    object has no setter（area 只读）
#
# 【预测先行·方案A：r 可写且校验，area 只读】
# d. c.r = -5     → ValueError: 半径不能为负（炸在存储量的 setter 上）
# e. c.r = 5 之后 c.area → 重算：3.14159 * 5**2 = 78.53975
#    （area 不存，每次读现算）
# f. c.area = 99  → AttributeError: property 'area' of 'Circle'
#                    object has no setter（area 天生只读，不接受写）
#
# 【选型判断·写进 r.setter 注释】
#   负半径是"调用者/外部输入错误"，不是"程序内部不变量"。
#   python -O 会整条删掉 assert，校验必须无条件生效 → 用 raise，不用 assert。
#   校验挂在存储量 r 上，不挂在派生量 area 上：派生量由存储量决定，天生只读。


class Circle:
    def __init__(self, r):
        self.r = r                      # 走下面的 r.setter，构造时就校验

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, value):
        # 选型判断：负半径是调用者/外部输入错误，不是内部不变量；
        # python -O 会删掉 assert，校验必须无条件生效 → 用 raise 不用 assert。
        # 校验挂在存储量 r 上——派生量 area 由它决定，不需要单独守。
        if value < 0:
            raise ValueError("半径不能为负")
        self._r = value

    @property
    def area(self):
        return 3.14159 * self.r ** 2
    # 不写 area.setter → area 天生只读


c = Circle(2)
print("a. c.area    =", c.area)

try:
    print("b. c.area()  =", c.area())
except Exception as e:
    print(f"b. {type(e).__name__}: {e}")

try:
    c.area = 99
    print("c. c.area = 99 → 成功了？ c.area =", c.area)
except Exception as e:
    print(f"c. {type(e).__name__}: {e}")

try:
    c.r = -5
    print("d. c.r = -5 → 成功了？ c.r =", c.r)
except Exception as e:
    print(f"d. {type(e).__name__}: {e}")

c.r = 5
print("e. c.r = 5 之后, c.area =", c.area, "（重算的）")

try:
    c.area = 99
    print("f. c.area = 99 → 成功了？ c.area =", c.area)
except Exception as e:
    print(f"f. {type(e).__name__}: {e}")

# 【对账】
# a. 命中：12.56636
# b. 命中：TypeError: 'float' object is not callable
# c. 命中：AttributeError: property 'area' of 'Circle' object has no setter
# d. 命中：ValueError: 半径不能为负
# e. 命中：78.53975（重算，不是原来的 12.56636）
# f. 命中：AttributeError: property 'area' of 'Circle' object has no setter
#    —— d 和 f 的对比就是本实验的核心：
#       d 炸在存储量 r 的 setter 上（校验路径）；
#       f 炸在派生量 area 没有 setter（只读路径）。
#       两条路各司其职，不再出现"名字叫 area、改的却是 r"的语义 bug。