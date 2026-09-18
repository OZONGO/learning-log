# dir_report.py
"""MP1 衍生小工具 · 目录体检器

## DoD（可命令验证）
1. `python dir_report.py <空目录>` 不抛 ZeroDivisionError：打印总文件数 0、总大小 0B，
   分布表给出“（无文件）”提示。
2. `python dir_report.py demo_dir` 分布表按总字节降序；同分时按扩展名字母序。
   表头含 扩展名／文件数／总字节／占比。
3. 同一目录下 `main.PY` 与 `main.py` 归入同一桶：键统一 `.lower()`。
4. 无扩展名文件的桶键在数据层是 `''`，展示层映射为 `(无扩展名)`。
5. 目录不计入统计：`rglob('*')` 结果先过 `is_file()`；子目录不出现、文件数不虚高。
6. `python dir_report.py <不存在的路径>` 不静默出报表：往 stderr 打一行错误，
   带上解析后的绝对路径，退出码 2。空目录不违反本条，仍走第 1 条。

## 预测（跑前先写，跑后对账）
### ① 空目录
    目录: <空目录>
    总文件数: 0
    总大小: 0B

    按扩展名分布: （无文件）

### ② demo_dir 造完样本后
    .py 桶 3 个（alpha.py + beta.py + D.PY）= 390B
    .txt 桶 1 个（sub/sub2/deep.txt）= 150B
    .md 桶 1 个（notes.md）= 45B
    '' 桶 1 个（LICENSE）= 36B
    总 6 文件 621B

### ③ python-100/
    预计 .py 桶最大（w1–w4 里多个 .py）；具体以实际为准。

## 结构
- collect_files：rglob('*') → 只留 is_file()
- tally：dict[扩展名] → Bucket(n, size)
- render_report：总数／总大小／按大小降序分布表，分母为 0 时不除。
- main：唯一碰外面的地方——解析参数、校验入口、决定退出码。
"""

from dataclasses import dataclass
from pathlib import Path
import sys
import unicodedata


NO_EXT_LABEL = "(无扩展名)"
EXIT_USAGE = 2          # 命令行用法错误：沿用 Unix 惯例（argparse 也用 2）
EXIT_OK = 0


@dataclass
class Bucket:
    n: int = 0
    size: int = 0


def check_root(root):
    """入口校验。返回错误消息；None 表示这个目录可以扫。

    为什么必须有：`rglob('*')` 对不存在的路径不抛异常，静默返回空。
    于是“拼错路径”和“目录真的空”在报表上长得一模一样——沉默型 bug。
    """
    resolved = root.resolve()      # 路径不存在时 resolve 也不抛（默认 strict=False）
    hint = f"\n  解析为: {resolved}"
    if not root.exists():
        return f"错误: 目录不存在: {root}{hint}"
    if not root.is_dir():
        return f"错误: 是文件不是目录: {root}{hint}"
    return None


def collect_files(root):
    """取清单：rglob('*') 拿全树，只留 is_file()。

    不过滤 is_file() 的话：目录也会进结果，Windows 上目录 st_size=0，
    文件数虚高、总大小不变——沉默型 bug 的完美配方。
    """
    return [p for p in root.rglob("*") if p.is_file()]


def tally(files):
    """记账：dict[扩展名] → Bucket(n, size)。

    键归一：.suffix.lower()；无扩展名用空串 '' 当键（事实层），
    展示标签在 render 层映射。
    """
    totals = {}
    for f in files:
        ext = f.suffix.lower()
        b = totals.setdefault(ext, Bucket())
        b.n += 1
        b.size += f.stat().st_size
    return totals


def display_ext(ext):
    """事实层键 → 展示层标签。空串是事实，标签是展示。"""
    return ext if ext else NO_EXT_LABEL


def _width(s):
    """显示宽度：CJK 全角字符占 2 列。"""
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in s)


def _pad(s, width, align="left"):
    """按显示宽度补空格。"""
    gap = max(0, width - _width(s))
    return s + " " * gap if align == "left" else " " * gap + s


def render_report(root, files, totals):
    """出报表：总数／总大小／按大小降序分布。返回字符串，不 print。"""
    lines = []
    total_size = sum(b.size for b in totals.values())

    lines.append(f"目录: {root}")
    lines.append(f"总文件数: {len(files)}")
    lines.append(f"总大小: {total_size}B")
    lines.append("")

    if not totals:
        lines.append("按扩展名分布: （无文件）")
        return "\n".join(lines) + "\n"

    lines.append("按扩展名分布（按总字节降序，同分按扩展名字母序）:")
    lines.append(
        _pad("扩展名", 14) + _pad("文件数", 8, "right")
        + _pad("总字节", 10, "right") + _pad("占比", 8, "right")
    )
    # 同分时按扩展名字母序：把“谁在前”从文件系统的偶然变成规则。
    for ext, b in sorted(totals.items(), key=lambda kv: (-kv[1].size, kv[0])):
        pct = b.size / total_size if total_size else 0.0
        lines.append(
            _pad(display_ext(ext), 14) + _pad(str(b.n), 8, "right")
            + _pad(str(b.size), 10, "right") + _pad(f"{pct:.1%}", 8, "right")
        )
    return "\n".join(lines) + "\n"


def main():
    if len(sys.argv) > 1:
        root = Path(sys.argv[1])
    else:
        root = Path(__file__).parent / "demo_dir"

    error = check_root(root)
    if error is not None:
        print(error, file=sys.stderr)     # 错误走 stderr，报表走 stdout，各走各的
        return EXIT_USAGE
    # 校验只问“能不能扫”，不问“扫出来几个”：空目录合法通过，落到 DoD 1。
    files = collect_files(root)
    totals = tally(files)
    print(render_report(root, files, totals), end="")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())