# python-100/ 目录说明

> 起草：AI ｜ 内容确认：OZONGO（2026-09-04 建立）

本目录是 W1-W9 的练习集合（02 文档约定：练习不建独立 repo，MP1-MP4 仍各自独立 repo）。
按周分目录，只分两层——项目级的再深就交给 MP 仓库。

| 目录 | 装什么 | 说明 |
|---|---|---|
| `w1/` | W1 三练习：guess_number / calculator / converter；numcheck.py（W3 把 converter 的校验抽成模块，2026-09-09 起） | 正式交付件（对应 02 文档 W1 交付）；numcheck ⚠ 必须与 converter **同目录**——import 只认调用者身边的模块文件 |
| `w2/` | word_freq（预习版 Top5）/ word_freq2（读文件 Top10）/ word_freq3（完整版：isdigit 闸＋Counter）/ score_analyzer（练习② 成绩单分析）/ sample.txt（《教父》开篇） | W2 三练习全齐；正式周会出 word_count.py |
| `w3/` | 函数与模块课：func_intro / func_default_args / try_except / scope_lab / args_lab / area_mod / use_area | 课中实验与最小示例（非交付件） |
| `playground/` | 概念实验：list_intro.py / dict_intro.py | 不验收、不交付，纯实验场 |

**运行要求**：含数据文件的程序（`w2/word_freq2.py`）在 `w2/` 目录下运行——它的数据路径是**相对路径** `sample.txt`，相对"你运行命令时所在的目录"，不是文件所在目录。这是 W5 正式学 `os.path` 前的第一次接触。

**命名习惯**：正式练习用小写单词+下划线（`word_count.py`）；预习/实验用 `xxx_intro.py`。
