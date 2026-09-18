# make_samples.py
"""造样本：给 dir_report.py 体检用。

五个基础样本（任务 2）+ 一个 D.PY（P2 补证据：验证 .lower() 归一桶）。

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

samples = {
    base / "alpha.py": "x = 1\n" * 10,            # 60B
    base / "beta.py": "print('hello')\n" * 20,    # 300B
    base / "D.PY": "y = 2\n" * 5,                 # 30B，验证大小写归一
    base / "notes.md": "# 标题\n" * 5,             # 45B（UTF-8）
    base / "LICENSE": "MIT License\n" * 3,         # 36B
    deep / "deep.txt": "deep file\n" * 15,         # 150B
}

for path, content in samples.items():
    path.write_text(content, encoding="utf-8")

print(f"造了 {len(samples)} 个样本，根目录: {base}")