# make_samples.py
"""造样本：给 dir_report.py 体检用。

五个基础样本（任务 2）+ 一个 D.PY（P2 补证据：验证 .lower() 归一桶）。
9/20 补：一对真同分的桶 first.bbb / second.aaa（测 DoD 2 后半条"同分按扩展名字母序"），
外加空目录靶 probe_empty（测 DoD 1）。现共 8 个文件样本 ＋ 1 个空目录。

深层目录：用 parents=True 兜中间层级。
理由：sub/sub2 是两层，不带 parents 会在 sub 不存在时 FileNotFoundError；
     脚本可能重复跑，exist_ok=True 让第二遍不炸。
     这正是上午 mkdir 那条判据：预期内（可能已存在）用预防，非预期让它抛。
"""
from pathlib import Path

base = Path(__file__).parent / "demo_dir"
base.mkdir(parents=True, exist_ok=True)

deep = base / "sub" / "sub2"
deep.mkdir(parents=True, exist_ok=True)

# DoD 1 的空目录靶：必须由脚本自己造。9/18 手工建的 probe_empty 到 9/20 已全盘搜不到——
# git 根本不跟踪空目录，"手工造的靶"等于不可复现的证据。空目录要保持空，所以不往里写任何东西。
probe = base.parent / "probe_empty"
probe.mkdir(parents=True, exist_ok=True)

samples = {
    # 注：下列注释原来的字节数是**逻辑长度**，盘上实测每个文件多出的字节数＝它的换行数
    # ——`write_text` 走文本模式，`"\n"` 被翻成 `"\r\n"`。对账：逻辑合计 621B ＋ 换行 58 = 盘上 679B。
    base / "alpha.py": "x = 1\n" * 10,            # 逻辑 60B → 盘上 70B
    base / "beta.py": "print('hello')\n" * 20,    # 逻辑 300B → 盘上 320B
    base / "D.PY": "y = 2\n" * 5,                 # 逻辑 30B → 盘上 35B，验证大小写归一
    base / "notes.md": "# 标题\n" * 5,             # 逻辑 45B（UTF-8）→ 盘上 50B
    base / "LICENSE": "MIT License\n" * 3,         # 逻辑 36B → 盘上 39B
    deep / "deep.txt": "deep file\n" * 15,         # 逻辑 150B → 盘上 165B
    # T32 尾债（9/20 补）：造一对**真同分**的桶，让 DoD 2 后半条"同分按扩展名字母序"有数据可测。
    # ①内容零换行 → 逻辑＝盘上＝40B，故意绕开上面那个 CRLF 陷阱，不靠巧合对齐；
    # ②文件名序与扩展名序**刻意相反**（`first.bbb` 名字在前、`.aaa` 扩展名在前），
    #   这样输出里谁先出现，就直接说明排序键吃的是扩展名还是文件名。
    base / "first.bbb": "B" * 40,                  # 盘上 40B
    base / "second.aaa": "A" * 40,                 # 盘上 40B
}

for path, content in samples.items():
    path.write_text(content, encoding="utf-8")

print(f"造了 {len(samples)} 个样本，根目录: {base}")