#json_lab.py


#实验1
import ast
import json
from datetime import datetime
from pathlib import Path

OUT = Path(__file__).parent

# ============================================================
# 实验 1 · 判据差反向验一次
# ============================================================
# 预测：
#   json.loads(repr({"ok": True}))
#     repr 产出 "{'ok': True}"  —— Python 字面量方言
#     json.loads 期望 JSON 方言
#     单引号不合法、True 不合法
#     → 预期 json.decoder.JSONDecodeError，报在解析层（不是 loads 之后）
#
#   ast.literal_eval('{"ok": true}')
#     双引号本身 Python 也认
#     但 true 会被 ast 解析成 Name 节点，不是字面量
#     → 预期 ValueError: malformed node or string
#
# 必答：两次失败各暴露了“字面量方言”的哪一半？
#   第一次：Python 方言里合法的东西（'...'、True）不是 JSON 方言。
#   第二次：JSON 方言里合法的东西（true）不是 Python 字面量。
#   两个方言是对称互斥的：对方的关键字，两边都认不出。
# ============================================================

def exp1():
    print("=" * 60)
    print("实验 1")
    print("=" * 60)

    try:
        json.loads(repr({"ok": True}))
    except Exception as e:
        print(f"json.loads(repr(...)) -> {type(e).__name__}: {e}")

    try:
        ast.literal_eval('{"ok": true}')
    except Exception as e:
        print(f"ast.literal_eval('{{\"ok\": true}}') -> {type(e).__name__}: {e}")


# ============================================================
# 实验 2 · 过桥死法清单
# ============================================================
# 预测：
#   一个 dict 同时塞 tuple / int 键 / set / datetime / inf / nan
#   dumps 会在遇到第一个不可序列化对象时抛错；dict 保持插入顺序，
#   所以先撞上谁取决于插入序 —— 我按 set 放最前来让它先炸。
#
#   逐个单独试时预期：
#     tuple       → 静默变 list，不抛
#     int 键      → 静默变 "1" 字符串键，不抛
#     set         → TypeError
#     datetime    → TypeError
#     inf / nan   → 默认 allow_nan=True，产出 Infinity / NaN
#                   这是非法 JSON（RFC 8259 不认），但 Python 自家
#                   loads 默认能读回 —— 造出非法 JSON 类
#
#   加 allow_nan=False 后 inf/nan 当场 ValueError。
#
# 必答：inf/nan 归到哪一组？为什么跟 9/11 “不兜炸出去才安全”同一条原则？
#   归到“造出非法 JSON”这一组（比“静默变形”更贵，比“当场抛错”更阴）。
#   暴露点离出错点最远：本机往返不崩，跨语言一读才炸。
#   allow_nan=False 就是把“跨机才暴露”提前到“本机写出那一刻”当场崩。
#   这正是 9/11 那条原则：宁可当场炸在源头，也不要把坏东西放出去兜一圈。
# ============================================================

def exp2():
    print("=" * 60)
    print("实验 2")
    print("=" * 60)

    d_all = {
        "s": {1, 2},
        "t": ("a", "b"),
        "1": "x",  # 单独测 int 键时再改成 {1: "x"}
        "dt": datetime(2024, 1, 1),
        "inf": float("inf"),
        "nan": float("nan"),
    }
    try:
        json.dumps(d_all)
    except Exception as e:
        print(f"(a) 混合 dumps -> {type(e).__name__}: {e}")

    cases = {
        "tuple": {"t": (1, 2)},
        "int_key": {1: "x"},
        "set": {"s": {1, 2}},
        "datetime": {"dt": datetime(2024, 1, 1)},
        "inf": {"x": float("inf")},
        "nan": {"x": float("nan")},
    }
    for name, obj in cases.items():
        try:
            s = json.dumps(obj)
            back = json.loads(s)
            print(f"(b) {name:<9} -> ok  s={s!r}  back={back!r}")
        except Exception as e:
            print(f"(b) {name:<9} -> {type(e).__name__}: {e}")

    for name in ("inf", "nan"):
        try:
            json.dumps({"x": float(name)}, allow_nan=False)
        except Exception as e:
            print(f"(c) {name} allow_nan=False -> {type(e).__name__}: {e}")


# ============================================================
# 实验 3 · 两道工序的互锁
# ============================================================
# 预测：
#   d = {"周次": "W3", "note": "中文"}
#
#   ① dumps(d) + encoding="utf-8"
#      ensure_ascii 默认 True → 中文变成 \uXXXX
#      整段只有 ASCII 字符，UTF-8 写出 → 纯 ASCII 字节
#
#   ② dumps(d, ensure_ascii=False) + encoding="utf-8"
#      中文原样保留，UTF-8 写出 → 中文字符是多字节
#
#   ③ ②的产物 + 不写 encoding
#      Windows 默认 cp936（GBK）
#      中文按 GBK 编字节 → 与 ② 的 UTF-8 字节不同
#
#   ④ ①的产物 + 不写 encoding
#      内容只有 ASCII，cp936 与 utf-8 对 ASCII 编出的字节相同
#      → ④ 与 ① 字节完全相同（差 0）
#
# 必答：④ 与 ① 字节是否相同？为什么“不写 encoding”在 ④ 上从没暴露过？
#   相同。① 的产物经 ensure_ascii=True 后只剩 ASCII 字符，
#   ASCII 在 cp936 / utf-8 / latin-1 下字节一致。
#   所以“不写 encoding”这个坏习惯在纯 ASCII 内容上永远看不见病，
#   只有内容里出现非 ASCII（如 ③）才发作。
# ============================================================

def exp3():
    print("=" * 60)
    print("实验 3")
    print("=" * 60)

    d = {"周次": "W3", "note": "中文"}

    f1 = OUT / "e3_1_ascii_utf8.json"
    f2 = OUT / "e3_2_raw_utf8.json"
    f3 = OUT / "e3_3_raw_default.json"
    f4 = OUT / "e3_4_ascii_default.json"

    s1 = json.dumps(d)
    s2 = json.dumps(d, ensure_ascii=False)

    f1.write_text(s1, encoding="utf-8")
    f2.write_text(s2, encoding="utf-8")
    f3.write_text(s2)  # 不写 encoding
    f4.write_text(s1)  # 不写 encoding

    b1, b2, b3, b4 = (p.read_bytes() for p in (f1, f2, f3, f4))
    print(f"① bytes: {b1}")
    print(f"② bytes: {b2}")
    print(f"③ bytes: {b3}")
    print(f"④ bytes: {b4}")
    print(f"|①-④| 长度差 = {abs(len(b1) - len(b4))}, 内容相同 = {b1 == b4}")
    print(f"|②-③| 长度差 = {abs(len(b2) - len(b3))}, 内容相同 = {b2 == b3}")


# ============================================================
# 实验 4 · 换行归因
# ============================================================
# 预测：
#   dumps(d) 单行               → 无真实 \n，盘上无 0d 0a
#   dumps(d, indent=2)          → indent 造出真实 \n
#                                 文本模式默认翻译 \n → \r\n
#                                 盘上出现 0d 0a
#   数据带 "a\nb" 且无 indent    → dumps 把字符串值里的 \n
#                                 转义成 \ 和 n 两个字符
#                                 盘上没有真实换行 → 无 0d 0a
#   indent=2 + newline=""        → 关闭 \n → \r\n 翻译
#                                 盘上只有 0a
#
# 必答：
#   0d 0a 出现几次、每次是谁造的？
#     只出现在 indent=2 那一次（不带 newline=""）；每个结构换行都翻一次。
#     一次换行 = 一个 0d 0a；谁造的：文本模式默认 newline=None 把 \n → os.linesep。
#
#   数据里那个 \n 在盘上以什么形态存在？
#     以“两个字符：反斜杠 + n”存在，不是真实换行。
#     json.dumps 在序列化字符串值时把它转义；文本模式的换行翻译看不见它，
#     因为它压根不是换行字节。
# ============================================================

def exp4():
    print("=" * 60)
    print("实验 4")
    print("=" * 60)

    d = {"a": 1, "b": 2}

    f_single = OUT / "e4_single.json"
    f_indent = OUT / "e4_indent.json"
    f_data_nl = OUT / "e4_data_nl.json"
    f_indent_nl = OUT / "e4_indent_newline_empty.json"

    f_single.write_text(json.dumps(d), encoding="utf-8")
    f_indent.write_text(json.dumps(d, indent=2), encoding="utf-8")
    f_data_nl.write_text(json.dumps({"note": "a\nb"}), encoding="utf-8")
    with open(f_indent_nl, "w", encoding="utf-8", newline="") as fp:
        fp.write(json.dumps(d, indent=2))

    for p in (f_single, f_indent, f_data_nl, f_indent_nl):
        b = p.read_bytes()
        print(f"{p.name:<32} bytes={b!r}  0d0a×{b.count(b'\r\n')}")


# ============================================================
# 实验 5 · MP1 前瞻
# ============================================================
# 预测：
#   d1 = {"a": 1, "b": 2}
#   d2 = {"b": 2, "a": 1}
#
#   (a) 只加 indent=2
#       dict 保留插入序 → dumps(d1) != dumps(d2)
#
#   (b) indent=2, sort_keys=True
#       键排序后结构相同 → dumps(d1) == dumps(d2)
#
# 必答：不加 sort_keys，MP1 周报 JSON 进 git 会制造什么？
#   假 diff。两次内容相同但插入序不同 → 字节不同 → git 显示“改动”，
#   但语义其实没变。噪声会掩盖真正的变更。
# ============================================================

def exp5():
    print("=" * 60)
    print("实验 5")
    print("=" * 60)

    d1 = {"a": 1, "b": 2}
    d2 = {"b": 2, "a": 1}

    a1 = json.dumps(d1, indent=2)
    a2 = json.dumps(d2, indent=2)
    b1 = json.dumps(d1, indent=2, sort_keys=True)
    b2 = json.dumps(d2, indent=2, sort_keys=True)

    print(f"(a) no sort_keys : a1==a2 -> {a1 == a2}")
    print(f"(b) sort_keys    : b1==b2 -> {b1 == b2}")


# ============================================================
# 实验 6 · 补 P1：GBK 字节被 UTF-8 读，是抛错还是乱码？
# ============================================================
# 预测：
#   f3 = e3_3_raw_default.json，盘上是 GBK 字节。
#   f3.read_text(encoding="utf-8")
#     \xd6\xdc 不是合法 UTF-8 序列 → 预测 UnicodeDecodeError
#   f3.read_text(encoding="gbk")
#     字节本来就是 GBK 写的 → 预测成功读回原字符串
#
# 必答：什么时候当场抛 UnicodeDecodeError、什么时候静默变乱码？
#   判据是目标编码对这段字节序列是否合法：
#   非法 → 当场 UnicodeDecodeError；
#   合法但映射到别的字符 → 静默乱码（例如 latin-1 读任何字节都不抛）。
# ============================================================

def exp6():
    print("=" * 60)
    print("实验 6")
    print("=" * 60)

    f3 = OUT / "e3_3_raw_default.json"

    try:
        print("utf-8 读:", f3.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"utf-8 读 -> {type(e).__name__}: {e}")

    try:
        print("gbk   读:", f3.read_text(encoding="gbk"))
    except Exception as e:
        print(f"gbk   读 -> {type(e).__name__}: {e}")


# ============================================================
# 实验 7 · 同一对编码，三种内容三种命运
# ============================================================
# 路径复用实验 3 的 ③：ensure_ascii=False + 不写 encoding
# → Windows 默认 cp936 写盘，再用 encoding="utf-8" 读回。
#
# 预测：
#   "W3"   → 盘上纯 ASCII。UTF-8 对 ASCII 区怎么读都对。
#            读回 '{"note": "W3"}'，完全正确。
#
#   "中文" → GBK 字节 \xd6\xd0\xce\xc4。
#            \xd6 = 11010110，UTF-8 看到 110 开头，期待一个
#            10xxxxxx 延续字节；下一个 \xd0 = 11010000，
#            不是延续字节 → UnicodeDecodeError。
#
#   "学习" → GBK 字节 \xd1\xa7\xcf\xb0。
#            \xd1\xa7 恰好构成合法 UTF-8 双字节序列；
#            \xcf\xb0 也恰好合法。
#            解码器不抛，但解出 'ѧϰ' —— 静默污染。
#
# 必答三句（跑完对账）：
# 1. 抛错判据不是“编码不匹配就抛”。
#    “学习”也不匹配，它没抛。真判据是：
#    这段字节序列在目标编码下是否构成合法序列。
#    UTF-8 是严格自校验编码，对每个字节的位模式有硬性规定；
#    GBK 字节碰巧拼成合法 UTF-8 序列时，解码器照收。
#
# 2. “没抛”不能当“读对了”的证据。
#    合法字节序列 ≠ 原内容。'ѧϰ' 就是反例：
#    程序继续跑，数据已经废了，且没有任何异常提醒你。
#
# 3. 同族收口（以你 9/18 原话为准，此处复述）：
#    炸不是必然、静默也不是偶然，换一段内容就可能翻转。
# ============================================================

def exp7():
    print("=" * 60)
    print("实验 7")
    print("=" * 60)

    cases = [
        ("W3", "w3"),
        ("中文", "zhongwen"),
        ("学习", "xuexi"),
    ]

    for content, tag in cases:
        p = OUT / f"e7_{tag}.json"
        p.write_text(json.dumps({"note": content}, ensure_ascii=False))  # 不写 encoding
        raw = p.read_bytes()
        print(f"内容={content!r}")
        print(f"  盘上 bytes: {raw}")
        try:
            s = p.read_text(encoding="utf-8")
            print(f"  utf-8 读回: {s!r}")
        except Exception as e:
            print(f"  utf-8 读 -> {type(e).__name__}: {e}")
        print()


if __name__ == "__main__":
    exp1()
    exp2()
    exp3()
    exp4()
    exp5()
    exp6()
    exp7()