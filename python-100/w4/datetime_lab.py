#datetime_lab.py


from datetime import date, datetime, timedelta, timezone
import time


def sep(title):
    print("\n" + "=" * 8, title, "=" * 8)


# ============================================================
# exp1 构造与拒收
# 预测：
# date(2026, 9, 27) -> 2026-09-27
# date(2026, 2, 31) -> ValueError: day is out of range for month
# date(2024, 2, 29) -> 2024-02-29
# date(1900, 2, 29) -> ValueError: day is out of range for month
# date(2000, 2, 29) -> 2000-02-29
# ============================================================
sep("exp1 构造与拒收")
print("正常构造:", date(2026, 9, 27))

for y, m, d in [(2026, 2, 31), (2024, 2, 29), (1900, 2, 29), (2000, 2, 29)]:
    try:
        val = date(y, m, d)
        print(f"date({y}, {m}, {d}) -> {val}")
    except ValueError as e:
        print(f"date({y}, {m}, {d}) -> ValueError: {e}")


# ============================================================
# exp2 点段走桥
# 预测：
# date(2026,10,4) - date(2026,9,27) -> timedelta(days=7)，类型 timedelta
# date(2026,9,27) + timedelta(days=3) -> 2026-09-30
# date(2026,12,31) + timedelta(days=1) -> 2027-01-01
# date(2024,2,28) + timedelta(days=1) -> 2024-02-29
# date 与 datetime 直接比较 -> TypeError
# timedelta(days=2) + timedelta(hours=3) -> 2 days, 3:00:00
# ============================================================
sep("exp2 点段走桥")

d1 = date(2026, 9, 27)
d2 = date(2026, 10, 4)
diff = d2 - d1
print("date - date:", diff, type(diff))

print("+3天:", d1 + timedelta(days=3))
print("跨年:", date(2026, 12, 31) + timedelta(days=1))
print("闰日:", date(2024, 2, 28) + timedelta(days=1))

try:
    print(date(2026, 9, 27) < datetime(2026, 9, 27, 13))
except TypeError as e:
    print("date 与 datetime 比较 -> TypeError:", e)

print("timedelta 相加:", timedelta(days=2) + timedelta(hours=3))


# ============================================================
# exp3 字符串双向
# 预测：
# strptime("2026-09-27", "%Y-%m-%d") -> 2026-09-27 00:00:00，类型 datetime
# strptime("2026-9-27", "%Y-%m-%d") -> 成功，2026-09-27 00:00:00
# strptime("2026-13-99", "%Y-%m-%d") -> ValueError
# strftime("%A") -> Sunday
# 中文格式 -> 2026年09月27日
# isoformat / fromisoformat -> 往返一致
# strptime("2026-09-27", "%Y-%M-%d") -> 静默错值，%M 是分钟，月份默认 1 月
# ============================================================
sep("exp3 字符串双向")

dt1 = datetime.strptime("2026-09-27", "%Y-%m-%d")
print("strptime 正常:", dt1, type(dt1))

try:
    dt2 = datetime.strptime("2026-9-27", "%Y-%m-%d")
    print("不补零:", dt2)
except ValueError as e:
    print("不补零 -> ValueError:", e)

try:
    dt3 = datetime.strptime("2026-13-99", "%Y-%m-%d")
    print("非法值:", dt3)
except ValueError as e:
    print("非法值 -> ValueError:", e)

print("strftime %A:", dt1.strftime("%A"))
print("中文格式:", dt1.strftime("%Y年%m月%d日"))

iso = dt1.isoformat()
back = datetime.fromisoformat(iso)
print("isoformat:", iso)
print("fromisoformat:", back)

try:
    dt4 = datetime.strptime("2026-09-27", "%Y-%M-%d")
    print("误用 %M:", dt4)
except ValueError as e:
    print("误用 %M -> ValueError:", e)


# ============================================================
# exp4 时间戳与 naive/aware
# 预测：
# datetime.now() -> 当前本地时间，naive
# .timestamp() -> 自 1970-01-01 00:00 UTC 起的秒数
# fromtimestamp() -> 往返回本地时间
# datetime.now(timezone.utc) -> 带 +00:00 的 aware UTC 时间
# naive 与 aware 直接比较 -> TypeError
# ============================================================
sep("exp4 时间戳与 naive/aware")

now = datetime.now()
print("now:", now)
print("timestamp:", now.timestamp())
print("fromtimestamp:", datetime.fromtimestamp(now.timestamp()))

utc_now = datetime.now(timezone.utc)
print("utc_now:", utc_now)

try:
    print("naive < aware:", now < utc_now)
except TypeError as e:
    print("naive 与 aware 比较 -> TypeError:", e)


# ============================================================
# exp5 timedelta 陷阱
# 预测：
# td = timedelta(hours=25)
# td.days -> 1
# td.seconds -> 3600
# td.total_seconds() -> 90000.0
# print(td) -> 1 day, 1:00:00
# ============================================================
sep("exp5 timedelta 陷阱")

td = timedelta(hours=25)
print("td.days:", td.days)
print("td.seconds:", td.seconds)
print("td.total_seconds():", td.total_seconds())
print("print(td):", td)


# ============================================================
# exp6 开放题：perf_counter vs datetime.now 测耗时
# 预测：
# perf_counter 更稳定，分辨率高，单调；
# datetime.now 可能为 0.0 或波动较大，受系统钟影响。
# ============================================================
sep("exp6 开放题")


def small_loop():
    s = 0
    for i in range(100000):
        s += i
    return s


for i in range(3):
    t0 = time.perf_counter()
    small_loop()
    t1 = time.perf_counter()
    print(f"perf_counter 第{i+1}次: {t1 - t0:.6f} 秒")

for i in range(3):
    t0 = datetime.now()
    small_loop()
    t1 = datetime.now()
    print(f"datetime.now 第{i+1}次: {(t1 - t0).total_seconds():.6f} 秒")


# ============================================================
# 对账栏
# ============================================================

# exp1 构造与拒收
# 我以为：2026-02-31、1900-02-29 会 ValueError；2024-02-29、2000-02-29 成功。
# 实际：一致。
# 因为：date 构造器按日历规则判月长和闰年；1900 能被 100 整除但不能被 400 整除，不是闰年；2000 能被 400 整除，是闰年。

# exp2 点段走桥
# 我以为：date - date 得 timedelta；加 timedelta 能跨月跨年；date 与 datetime 直接比会 TypeError。
# 实际：一致。
# 因为：点减点得段，点加段回点；date 和 datetime 是不同类型，不自动折算，比较直接 TypeError。

# exp3 字符串双向
# 我以为：strptime 吃字符串吐对象，strftime 反向；%M 误用会出事。
# 实际：2026-9-27 成功；2026-13-99 报 ValueError；%M 枪输出 2026-01-27 00:09:00。
# 因为：%m 解析月份数字，不强制两位；非法月份被拒；%M 是分钟，吃掉了 09，月份没被赋值，默认 1 月。
#
# 三处补答：
# 1) %M 枪“月份默认 1 月”：是推的，不是查到的，也不是纯蒙。
#    依据：strptime 按格式码逐段填字段；模式里没有 %m，所以 month 没有输入；
#    datetime 未提供的字段取默认值，month 默认 1。%M 把 09 当分钟，所以得到
#    2026-01-27 00:09:00。
# 2) 不补零预测成功：是推的/有依据的猜。
#    依据：%m 表示月份数字，解析器通常接受 1-2 位数字，不要求前导零。
#    这个规则课上没讲，属于根据“数字段按数值解析”的推测。
# 3) timestamp 量级验算：
#    一年约 365.25 天 × 86400 秒 ≈ 31,557,600 秒。
#    2026-09-27 距 1970-01-01 约 56.7 年。
#    56.7 × 31,557,600 ≈ 1.79×10^9 秒。
#    1790488235.67 约 1.79e9，量级正确。

# exp4 时间戳与 naive/aware
# 我以为：timestamp() 是 1970-01-01 UTC 起秒数；naive 与 aware 不能比。
# 实际：一致。
# 因为：timestamp() 是全球同一时刻的秒数表示；naive 没写时区，aware 带 tzinfo，
# Python 拒绝跨时区猜。

# exp5 timedelta 陷阱
# 我以为：td.days=1，td.seconds=3600，total_seconds=90000.0，print=1 day, 1:00:00。
# 实际：一致。
# 因为：timedelta 内部规范化为（天、秒、微秒），.seconds 只表示去掉天数后的剩余秒数；
# 总秒数必须用 total_seconds()。

# exp6 开放题
# 我以为：perf_counter 更稳；datetime.now 可能波动甚至为 0。
# 实际：perf_counter 三次 0.0028-0.0032，稳定；
# datetime.now 三次 0.003848 / 0.004994 / 0.002744，最快最慢差约 80%。
# “可能为 0”没发生。
# 因为：perf_counter 是单调钟；datetime.now 是墙上时钟，可能被 NTP 校时。
#
# monotonic 的意思：单调，只增不减，never goes backward；不受系统墙上时钟调整影响。
#
# 为什么 now() 三次没撞上危险：
# 三次 3ms 循环窗口极短，NTP 校时是低概率事件，几乎不可能正好落在这三个窗口里。
# 没发生不代表安全；三次采样既证不了 now() 安全，也证伪不了它危险。
# 真正该信的是 perf_counter 的单调保证，不是运气。