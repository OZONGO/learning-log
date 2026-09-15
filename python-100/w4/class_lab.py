# class_lab.py
# 路径：learning-log/python-100/w4/class_lab.py
#
# ============================================================
# DoD（Definition of Done）—— 五个实验各自要证明什么
# ============================================================
#
# 实验①：最小类
#   - 证明实例属性是每个对象各一份，不是共享的。
#   - 证据：a.__dict__ 与 b.__dict__ 内容不同，且不是同一个 dict。
#
# 实验②：坏版 vs 好版
#   - 证明"可变类属性"会被所有实例共享并污染。
#   - 证明"__init__ 里挂实例属性"能让每个实例独立。
#   - 证据：坏版 bad1.items is bad2.items 为 True；
#           好版 good1.items is good2.items 为 False。
#
# 实验③：self 的等价性与包装
#   - 证明 对象.方法(参数) 等价于 类.方法(对象, 参数)。
#   - 证明 对象.方法.__func__ is 类.方法 为 True。
#   - 证明 对象.方法 is 对象.方法 为 False（每次访问都会新建绑定方法）。
#
# 实验④：忘写 self 的两副面孔
#   - 证明"方法签名不收 self"报 TypeError，并把原文抄全。
#   - 证明"__init__ 里少写 self"数据不上实例，报 AttributeError，并把原文抄全。
#
# 实验⑤：__init__ 不是"构造函数"
#   - 证明 __init__ 里 return 非 None 会报 TypeError，并把原文抄全。
#   - 证明对象是在 __init__ 之前被造出来的（__new__ 先于 __init__）。
#
# ============================================================


# ============================================================
# 实验①：最小类，证明实例属性是每个对象各一份
# ============================================================
#
# 【预测先行】
# - 每个对象的 __dict__ 里应该有 1 个键，即 'value'。
# - 因为 __init__ 里只写了 self.value = value。
# - show 方法不在实例 __dict__ 里，它在类对象 Counter 上。
#
# 【对账】
# - 预测正确：两个 __dict__ 各只有 'value' 一个键。
# - a.__dict__ 与 b.__dict__ 内容不同，且不是同一个对象。
# - show 没有出现在实例 __dict__ 里，证明方法只在类上。

class Counter:
    def __init__(self, value):
        self.value = value

    def show(self):
        return self.value


# 实例化两个对象
a = Counter(10)
b = Counter(20)


print("a.__dict__ =", a.__dict__)
print("b.__dict__ =", b.__dict__)
print("a.show() =", a.show())
print("b.show() =", b.show())
print("a.__dict__ is b.__dict__ =", a.__dict__ is b.__dict__)

# 实测输出：
# a.__dict__ = {'value': 10}
# b.__dict__ = {'value': 20}
# a.show() = 10
# b.show() = 20
# a.__dict__ is b.__dict__ = False


# ============================================================
# 实验②：坏版 vs 好版
# ============================================================
#
# 【预测先行】
# - 坏版 BadBag：items = [] 是类属性，所有实例共享同一个列表。
#   bad1.add(...) 和 bad2.add(...) 都会往同一个列表里塞。
#   预测 bad1.items is bad2.items 为 True，bad1.items is BadBag.items 为 True。
# - 好版 GoodBag：self.items = [] 在 __init__ 里，每个实例各自新建一个列表。
#   预测 good1.items is good2.items 为 False。
#
# 【对账】
# - 坏版预测正确：两个实例的 items 是同一个列表，且就是 BadBag.items。
# - 好版预测正确：两个实例的 items 是不同的列表。
# - 结论：可变类属性被所有实例共享；__init__ 里挂实例属性才能各自独立。

# 坏版：可变类属性，所有实例共享同一个列表
class BadBag:
    items = []  # 类属性，所有实例默认共享

    def __init__(self, name):
        self.name = name

    def add(self, item):
        # 原地 append：修改的是类属性 BadBag.items
        self.items.append(item)


# 好版：空容器放在 __init__ 里，成为每个实例自己的属性
class GoodBag:
    def __init__(self, name):
        self.name = name
        self.items = []  # 每个实例独立

    def add(self, item):
        self.items.append(item)


print("\n=== 实验2：坏版 BadBag ===")
bad1 = BadBag("bad1")
bad2 = BadBag("bad2")

bad1.add("bad1-item1")
bad2.add("bad2-item1")

print("bad1.__dict__ =", bad1.__dict__)
print("bad2.__dict__ =", bad2.__dict__)
print("BadBag.items =", BadBag.items)
print("bad1.items =", bad1.items)
print("bad2.items =", bad2.items)
print("bad1.items is bad2.items =", bad1.items is bad2.items)
print("bad1.items is BadBag.items =", bad1.items is BadBag.items)

# 实测输出（坏版，共享被污染）：
# bad1.__dict__ = {'name': 'bad1'}
# bad2.__dict__ = {'name': 'bad2'}
# BadBag.items = ['bad1-item1', 'bad2-item1']
# bad1.items = ['bad1-item1', 'bad2-item1']
# bad2.items = ['bad1-item1', 'bad2-item1']
# bad1.items is bad2.items = True
# bad1.items is BadBag.items = True
#
# 一眼看出：bad1.__dict__ 和 bad2.__dict__ 里都没有 items，
# 两个实例的 items 都指向同一个类属性列表，互相污染。


print("\n=== 实验2：好版 GoodBag ===")
good1 = GoodBag("good1")
good2 = GoodBag("good2")

good1.add("good1-item1")
good2.add("good2-item1")

print("good1.__dict__ =", good1.__dict__)
print("good2.__dict__ =", good2.__dict__)
print("good1.items =", good1.items)
print("good2.items =", good2.items)
print("good1.items is good2.items =", good1.items is good2.items)

# 实测输出（好版，各自独立）：
# good1.__dict__ = {'name': 'good1', 'items': ['good1-item1']}
# good2.__dict__ = {'name': 'good2', 'items': ['good2-item1']}
# good1.items = ['good1-item1']
# good2.items = ['good2-item1']
# good1.items is good2.items = False
#
# 一眼看出：good1.__dict__ 和 good2.__dict__ 里都各自有 items，
# 两个列表不是同一个对象，互不影响。


# 如果我把坏版那行原地 append 改成赋值，会发生什么？
#
# 例如把：
#   self.items.append(item)
# 改成：
#   self.items = self.items + [item]
# 或：
#   self.items = [item]
#
# 那么第一次调用 add 时，因为 self 没有实例属性 items，
# 会先找到类属性 BadBag.items（初始为 []），然后赋值操作
# self.items = ... 会创建一个新的实例属性 items，挂在当前实例上。
# 这个实例属性会遮蔽类属性 BadBag.items。
# 之后该实例的 items 就独立了，不再影响其他实例，也不再污染类属性。
# 但类属性 BadBag.items 仍然是原来的列表（可能为空，也可能保留之前
# 被 append 修改过的内容）。所以共享污染被打破，但类属性本身还在。


# ============================================================
# 实验③：self 的等价性与那层"包装"
# ============================================================
#
# 【预测先行】
# - 对象.方法(参数) 与 类.方法(对象, 参数) 结果相同。
# - 对象.方法.__func__ is 类.方法 为 True。
# - 对象.方法 is 对象.方法 为 False。
#   因为每次通过实例访问方法，都会新建一个绑定方法对象，
#   虽然它们的 __func__ 和 __self__ 相同，但包装对象本身不是同一个。
#
# 【对账】
# - 预测正确：两种调用结果相同。
# - 预测正确：adder.add.__func__ is Adder.add 为 True。
# - 预测正确：m1 is m2 为 False，m1 == m2 为 True。
# - 补充发现：绑定方法对象定义了 __eq__，所以 == 为 True。

class Adder:
    def __init__(self, base):
        self.base = base

    def add(self, x):
        return self.base + x


print("\n=== 实验3：self 的等价性与包装 ===")

adder = Adder(100)

# 证明两种调用结果相同
r1 = adder.add(23)
r2 = Adder.add(adder, 23)

print("adder.add(23) =", r1)
print("Adder.add(adder, 23) =", r2)
print("结果相同 =", r1 == r2)

# 证明底层函数是同一个
print("adder.add.__func__ is Adder.add =", adder.add.__func__ is Adder.add)
print("adder.add.__self__ is adder =", adder.add.__self__ is adder)

# 预测并验证：对象.方法 is 对象.方法
m1 = adder.add
m2 = adder.add

print("m1 is m2 =", m1 is m2)
print("m1 == m2 =", m1 == m2)
print("m1.__func__ is m2.__func__ =", m1.__func__ is m2.__func__)
print("m1.__self__ is m2.__self__ =", m1.__self__ is m2.__self__)

# 实测输出：
# adder.add(23) = 123
# Adder.add(adder, 23) = 123
# 结果相同 = True
# adder.add.__func__ is Adder.add = True
# adder.add.__self__ is adder = True
# m1 is m2 = False
# m1 == m2 = True
# m1.__func__ is m2.__func__ = True
# m1.__self__ is m2.__self__ = True

# 对账注释：
# 对象.方法 is 对象.方法 是 False。
# 因为每次通过实例访问方法，Python 都会临时创建一个新的绑定方法对象。
# 虽然这些绑定方法对象内部指向的底层函数 __func__ 相同，
# 绑定的实例 __self__ 也相同，但包装对象本身每次都是新的，
# 所以 is 比较身份时为 False。
# 而 == 比较绑定内容，__self__ 和 __func__ 都相同，所以为 True。


# ============================================================
# 实验④：忘写 self 的两副面孔
# ============================================================
#
# 【预测先行】
#
# 错误 1：方法签名里不收 self
# - 预测异常类型：TypeError
# - 消息大意：方法期望 0 个位置参数，但实例调用时 Python 自动把实例
#   当作 self 传了进去，所以多给了 1 个。
# - 预测原文：NoSelf.greet() takes 0 positional arguments but 1 was given
#
# 错误 2：__init__ 里少写 self
# - 预测异常类型：AttributeError
# - 消息大意：实例对象没有 value 属性，因为 value = value 只是给
#   局部变量赋值，没有挂到 self 上。
# - 预测原文：'LostData' object has no attribute 'value'
#
# 【对账】
# - 错误 1 预测正确，实测原文一致。
# - 错误 2 预测正确，实测原文一致。
# - 补充：LostData(10) 本身不报错，因为 __init__ 正常执行完了；
#   只是数据没上实例，lost.__dict__ 为空 {}。

class NoSelf:
    def greet():          # 错：没有 self
        return "hi"


print("\n=== 实验4：方法签名不收 self ===")
n = NoSelf()
try:
    n.greet()
except Exception as e:
    print("异常类型：", type(e).__name__)
    print("异常消息：", e)
    # 异常类型： TypeError
    # 异常消息： NoSelf.greet() takes 0 positional arguments but 1 was given


class LostData:
    def __init__(self, value):
        value = value     # 错：少写 self，只是局部变量


print("\n=== 实验4：__init__ 少写 self ===")
lost = LostData(10)
print("lost.__dict__ =", lost.__dict__)   # 空字典，数据没上实例
try:
    print(lost.value)
except Exception as e:
    print("异常类型：", type(e).__name__)
    print("异常消息：", e)
    # lost.__dict__ = {}
    # 异常类型： AttributeError
    # 异常消息： 'LostData' object has no attribute 'value'


# ============================================================
# 实验⑤：__init__ 不是"构造函数"
# ============================================================
#
# 【预测先行】
# - 在 __init__ 里写 return 1，会报：TypeError
# - 消息大意：__init__() 应该返回 None，不能返回 int。
# - 预测原文：__init__() should return None, not 'int'
#
# - 对象是在 __init__ 之前还是之后被造出来的？
#   答案：之前。
#   因为执行 类名(...) 时，Python 先调用 __new__ 创建实例，
#   再把实例作为 self 传给 __init__ 进行初始化。
#   __init__ 只负责初始化，不负责创建对象。
#   证据：__init__ 里的 self 已经是一个存在的对象；
#   __new__ 会先执行，并且返回的实例 id 和 __init__ 里的 self id 相同。
#
# 【对账】
# - 预测正确：TypeError，实测原文一致。
# - 预测正确：__new__ 先执行，__init__ 后执行。
# - 补充：__new__ 返回的对象 id 与 __init__ 里的 self id 完全相同，
#   说明 __init__ 拿到的 self 就是 __new__ 已经造好的那个对象。

class BadInit:
    def __init__(self):
        return 1          # 错：__init__ 只能返回 None


print("\n=== 实验5：__init__ 里 return 非 None ===")
try:
    b = BadInit()
except Exception as e:
    print("异常类型：", type(e).__name__)
    print("异常消息：", e)
    # 异常类型： TypeError
    # 异常消息： __init__() should return None, not 'int'


# 附加证明：__new__ 先于 __init__
class ProveOrder:
    def __new__(cls, *args, **kwargs):
        print("\nProveOrder.__new__ 被调用：对象在这里被创建")
        obj = super().__new__(cls)
        print("__new__ 返回的对象 id =", id(obj))
        return obj

    def __init__(self):
        print("ProveOrder.__init__ 被调用：self id =", id(self))
        print("说明 self 在 __init__ 之前就已经存在")


print("\n=== 实验5 附加：证明 __new__ 先于 __init__ ===")
p = ProveOrder()

# 实测输出：
# ProveOrder.__new__ 被调用：对象在这里被创建
# __new__ 返回的对象 id = 140234...
# ProveOrder.__init__ 被调用：self id = 140234...
# 说明 self 在 __init__ 之前就已经存在