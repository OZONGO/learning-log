#pathlib_lab.py


from pathlib import Path

# ========== 实验 1｜自我介绍 ==========
print("实验 1")
p = Path(__file__)

print("p.name:", p.name)
print("p.suffix:", p.suffix)
print("p.stem:", p.stem)
print("p.parent:", p.parent)
print("p.parent.parent:", p.parent.parent)
print("p.is_file():", p.is_file())
print("p.exists():", p.exists())

# 预测：p.startswith("E") 是事故，不是返回值。
# 报 AttributeError: 'WindowsPath' object has no attribute 'startswith'
# 因为 Path 不是 str，没有 startswith 方法。
try:
    print(p.startswith("E"))
except Exception as e:
    print("p.startswith('E') 报错:", type(e).__name__, e)

# 预测：str(p).startswith("E") 返回 True。
# 因为先 str(p) 转成普通字符串，字符串有 startswith。
print("str(p).startswith('E'):", str(p).startswith("E"))

# ========== 实验 2｜/ 拼接，纯计算不碰盘 ==========
print("\n实验 2")
root = Path("data")
target = root / "reports" / "report.txt"

# 预测：① Windows 上 print 出来分隔符是 \，即 data\reports\report.txt
# ② "data" / "reports" 会报 TypeError，因为 str 没实现 __truediv__
# ③ 从哪个目录跑输出都一样，因为只是构造 Path 对象，不碰盘、不 resolve、不依赖 CWD
print("target:", target)
print("type(target):", type(target))

try:
    print("data" / "reports")
except Exception as e:
    print('"data" / "reports" 报错:', type(e).__name__, e)

# ========== 实验 3｜安全创建 ==========
print("\n实验 3")
base = Path(__file__).parent
demo_dir = base / "demo_dir"
print("demo_dir:", demo_dir)

# 预测：第一遍创建成功；第二遍 exist_ok=True 不报错，返回 None。
demo_dir.mkdir(parents=True, exist_ok=True)
demo_dir.mkdir(parents=True, exist_ok=True)
print("demo_dir 已创建，两次 mkdir(parents=True, exist_ok=True) 均无异常")

# 另起子目录，裸 mkdir 两遍。
sub = demo_dir / "sub"
# 预测：第一遍成功；第二遍裸 mkdir 抛 FileExistsError。
sub.mkdir()
print("第一次裸 mkdir 成功")

try:
    sub.mkdir()
    print("第二次裸 mkdir 成功（预测错误）")
except Exception as e:
    print("第二次裸 mkdir 报错:", type(e).__name__, e)
# 这个报错在程序里应该兜还是不该兜？
# 如果“已存在”是预期内正常情况，应该用 exist_ok=True 预防，不该用 try 兜。
# 如果“已存在”是异常情况，就让它抛。assert 课那把试金石：预期内用预防，非预期用抛。

# ========== 实验 4｜glob vs rglob ==========
print("\n实验 4")
python100 = Path(__file__).parent.parent
print("python100:", python100)

glob_files = list(python100.glob("*.py"))
rglob_files = list(python100.rglob("*.py"))

print("glob('*.py') 个数:", len(glob_files))
for f in glob_files:
    print("  glob:", f.relative_to(python100))

print("rglob('*.py') 个数:", len(rglob_files))
for f in rglob_files:
    print("  rglob:", f.relative_to(python100))

# 预测：rglob 数大。glob 不递归，w1/w2/w3 等子目录里的 .py 在 glob 眼里不存在。
# 差的就是子目录里的 .py 文件。

# ========== 实验 5｜read_text/write_text 往返 + 编码现形 ==========
print("\n实验 5")
note = demo_dir / "note.txt"
note.write_text("圆面积＝πr²，值 78.54", encoding="utf-8")
print("写入 note.txt 完成")

# ① 带 encoding="utf-8"
text_utf8 = note.read_text(encoding="utf-8")
print("read_text(encoding='utf-8'):", text_utf8)

# ② 不带 encoding
# 预测：Windows 默认编码是 GBK；盘上是 UTF-8 字节；用 GBK 解码 UTF-8 字节会报 UnicodeDecodeError。
try:
    text_default = note.read_text()
    print("read_text() 不带 encoding:", text_default)
except Exception as e:
    print("read_text() 不带 encoding 报错:", type(e).__name__, e)

# ③ 删除并验证 exists
note.unlink()
print("note.exists() after unlink:", note.exists())
print("demo_dir 保留:", demo_dir.exists())