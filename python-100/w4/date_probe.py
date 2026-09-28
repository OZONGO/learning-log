#date_probe.py


import sys
from datetime import date, datetime


def ver(section):
    print(f"\n=== 段{section} | {sys.version} ===")


def probe_fromisoformat(s):
    try:
        return f"OK -> {date.fromisoformat(s)!r}"
    except Exception as e:
        return f"REJ -> {type(e).__name__}: {e}"


def probe_strptime(s):
    try:
        return f"OK -> {datetime.strptime(s, '%Y-%m-%d').date()!r}"
    except Exception as e:
        return f"REJ -> {type(e).__name__}: {e}"


# ============================================================
# 段 1
# 预测：
# "2026-01-01": A OK, B OK
# "20261129": A OK -> 2026-11-29, B REJ
# "2026-W48-3": A OK -> 2026-11-25, B REJ
# "2026-1-1": A REJ（要求补零）, B OK -> 2026-01-01
# 不对称对照：basic/周日期只有 A 放行；不补零只有 B 放行。
# ============================================================
ver(1)
for s in ["2026-01-01", "20261129", "2026-W48-3", "2026-1-1"]:
    print(f"{s!r:18} A: {probe_fromisoformat(s)}")
    print(f"{'':18} B: {probe_strptime(s)}")


# ============================================================
# 段 2
# 预测：
# "20２6-09-28": B OK -> 2026-09-28（%Y 的 \d 吃全角 ２，int 归一化）
# "２０２６-０９-２８": B REJ（%m/%d 正则主要写 ASCII 数字，不吃全角月/日）
# "2026-０９-28": B REJ（月段全角，%m 不吃）
# 三枪结果不一定一样：松缝主要在 %Y，不在 %m/%d 的普通分支。
# ============================================================
ver(2)
for s in ["20２6-09-28", "２０２６-０９-２８", "2026-０９-28"]:
    print(f"{s!r:24} B: {probe_strptime(s)}")


# 段2 补枪预测：
# "2026-01-1２"  → B 收 → 2026-01-12
#     %d 正则里有 [12]\d 这一支：'1' 匹配 [12]，'２' 匹配裸 \d（Unicode Nd）
# "2026-01-２２" → B 拒
#     '２' 不匹配 %d 任何分支的首字符（[12]/3/0/[1-9] 全是 ASCII）
for s in ["2026-01-1２", "2026-01-２２"]:
    print(f"{s!r:24} B: {probe_strptime(s)}")


# ============================================================
# 段 3
# 预测：
# "²": isdigit=True, isdecimal=False, isascii=False, int() -> ValueError
# "２": isdigit=True, isdecimal=True, isascii=False, int() -> 2
# "٣": isdigit=True, isdecimal=True, isascii=False, int() -> 3
# 能混进 %Y 的是 isdecimal()/Nd 这一类；"²" 是 No，不匹配 \d。
# ============================================================
ver(3)
for ch in ["²", "２", "٣"]:
    try:
        n = int(ch)
        int_result = f"OK -> {n}"
    except Exception as e:
        int_result = f"REJ -> {type(e).__name__}: {e}"
    print(
        f"{ch!r}: isdigit={ch.isdigit()}, "
        f"isdecimal={ch.isdecimal()}, "
        f"isascii={ch.isascii()}, "
        f"int={int_result}"
    )


# ============================================================
# 段 4
# 预测：
# "2026": 长度 4 -> 长度错误，不炸
# "2026-09-28 ": 长度 11 -> 长度错误，不炸
# "2026-09-2_8": 长度 11 -> 长度错误（注意不是字符集分支）
# "": 长度 0 -> 长度错误，空串走长度分支
# ============================================================
def date_shape_error(text):
    if len(text) != 10:
        return f"长度 {len(text)}，应为 10（YYYY-MM-DD）"
    if text[4] != "-" or text[7] != "-":
        return f"分隔符位置不对：{text!r}"
    for p in (text[0:4], text[5:7], text[8:10]):
        if not (p.isascii() and p.isdigit()):
            return f"{text!r} 含非 ASCII 数字"
    return None


ver(4)
for s in ["2026", "2026-09-28 ", "2026-09-2_8", ""]:
    print(f"{s!r:18} -> {date_shape_error(s)!r}")


# ============================================================
# 段 5
# 预测：
# "2026-02-28": None
# "2026-02-29": REJ day is out of range for month
# "2024-02-29": None
# "2026-02-30": REJ day is out of range for month
# "2026-13-99": REJ month must be in 1..12
# ============================================================
def date_error(text):
    error = date_shape_error(text)
    if error:
        return error
    try:
        date.fromisoformat(text)
    except ValueError as e:
        return f"日期 {text!r} 不是合法日历日：{e}"
    return None


ver(5)
for s in ["2026-02-28", "2026-02-29", "2024-02-29", "2026-02-30", "2026-13-99"]:
    print(f"{s!r:18} -> {date_error(s)!r}")


# ============================================================
# 段 6
# 预测：
# bad: "2026-13-99" -> None（静默当合法）
# good: "2026-13-99" -> 日期 '2026-13-99' 不是合法日历日：month must be in 1..12
# ============================================================
def bad_date_error(text):
    error = date_shape_error(text)
    if error:
        return error
    try:
        date.fromisoformat(text)
    except ValueError:
        return None
    return None


ver(6)
s = "2026-13-99"
print(f"bad_date_error({s!r}) -> {bad_date_error(s)!r}")
print(f"date_error({s!r})     -> {date_error(s)!r}")


# ============================================================
# 对账栏（已填，实测于 3.13.15）
# 运行版本：3.13.15 (tags/v3.13.15:4061bc4, Aug  5 2026, 13:05:39)
# [MSC v.1944 64 bit (AMD64)]
# ============================================================
# 段1 实际：与预测一致。
#   A 收 "2026-01-01" / "20261129" / "2026-W48-3"；
#   B 收 "2026-01-01" / "2026-1-1"。
#   不对称对照成立：basic 与周日期只有 A 放行；不补零只有 B 放行。
#
# 段2 实际（旧句，先留着）：
#   本次三枪里，松缝由 %Y 的年段单独显现；月段全角被挡。
#
# 段2 实际（补枪后新句，旧句写窄在哪）：
#   旧句写窄在哪——只测了"年段全角被收、月段全角被拒"就下结论
#   "松缝只在 %Y"。补枪后 %d 的 [12]\d 一支也吃 Nd：首位是 ASCII
#   1/2 时，次位可以是全角数字，B 静默收下。所以正确的口径是：
#   松缝出现在"那一支正则里出现裸 \d"的位置——%Y 有 4 支裸 \d，
#   %d 有 [12]\d 一支，%m 全是 ASCII 字面量／[0-9] 类，零裸 \d。
#
# 段2 补枪实际（预测已写、跑完按此核对）：
#   '2026-01-1２'  B: OK -> 2026-01-12（%d 的 [12]\d 吃全角 ２）
#   '2026-01-２２' B: REJ（'２' 不匹配 %d 任一分支首字符）
#
# 段3 实际：与预测一致。
#   '²': isdigit=True,  isdecimal=False, isascii=False, int=REJ
#   '２': isdigit=True,  isdecimal=True,  isascii=False, int=OK -> 2
#   '٣': isdigit=True,  isdecimal=True,  isascii=False, int=OK -> 3
#   能混进 %Y 的是 Nd / isdecimal 这一类；'²' 是 No，不进 \d。
#
# 段4 实际：与预测一致。
#   '2026'            -> 长度 4
#   '2026-09-28 '     -> 长度 11
#   '2026-09-2_8'     -> 长度 11
#   ''                -> 长度 0
#   四个输入全部先走长度分支；空串也走 len==0；校验器自己没炸。
#
# 段5 实际：与预测一致。
#   '2026-02-28' -> None
#   '2026-02-29' -> day is out of range for month
#   '2024-02-29' -> None
#   '2026-02-30' -> day is out of range for month
#   '2026-13-99' -> month must be in 1..12
#   关卡二真在办事：闰年、月末、月份越界都命中了。
#
# 段6 实际：与预测一致。
#   bad_date_error('2026-13-99') -> None
#   date_error('2026-13-99')     -> "日期 '2026-13-99' 不是合法日历日：month must be in 1..12"
#   常见错误 3 现场成立：except ValueError: return None 会沉默地把拒收当合法。
# ============================================================