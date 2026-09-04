# python-100/ 目录说明

> 起草：AI ｜ 内容确认：OZONGO（2026-09-04 建立）

本目录是 W1-W9 的练习集合（02 文档约定：练习不建独立 repo，MP1-MP4 仍各自独立 repo）。
按周分目录，只分两层——项目级的再深就交给 MP 仓库。

| 目录 | 装什么 | 说明 |
|---|---|---|
| `w1/` | W1 三练习：guess_number / calculator / converter | 正式交付件（对应 02 文档 W1 交付） |
| `w2/` | 词频统计两版：word_freq（预习版 Top5）/ word_freq2（读文件 Top10）+ sample.txt（《教父》开篇） | W2 练习① 的前置版；正式周会出 word_count.py |
| `playground/` | 概念实验：list_intro.py / dict_intro.py | 不验收、不交付，纯实验场 |

**运行要求**：含数据文件的程序（`w2/word_freq2.py`）在 `w2/` 目录下运行——它的数据路径是**相对路径** `sample.txt`，相对"你运行命令时所在的目录"，不是文件所在目录。这是 W5 正式学 `os.path` 前的第一次接触。

**命名习惯**：正式练习用小写单词+下划线（`word_count.py`）；预习/实验用 `xxx_intro.py`。
