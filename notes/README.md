# notes/ 使用说明

本目录只记录**后续复习时重要的内容**：概念卡、易错点、疑问的答案。

- 不记学习过程流水账（那是 docs/07 看板 Done Log 的职责）
- 讲义/文档原文可查的内容不重复抄录，只记原文之外的增量
- 命名建议：按主题如 `lecture-01-notes.md`、`python-坑集.md`

---

## 笔记索引（AI 维护；正文由本人写）

| 文件 | 主题 | 日期 | 状态 |
|---|---|---|---|
| `first-session.md` | 变量是标签不是盒子、`input()` 返回 str、f-string 与 `:.2f` | 2026-09-02 | 完成 |
| `python-流程控制.md` | bool 与比较、`//` `%` `**`、and/or/not、if-elif-else、while+break/continue、for+range | 2026-09-02 | 完成 |
| `python-输入校验与字符串陷阱.md` | `isdigit()` 门卫、字符串不可变、沉默型 bug、自定校验规则 | 2026-09-03 | 完成 |
| `python-容器与词频统计.md` | list 可变/tuple 不可变、切片左闭右开、enumerate 解包、dict 哈希与键不可变、sorted+key/lambda、词频统计三拼图 | 2026-09-04 | 完成（正文誊自当日口答） |
| `python-容器进阶与词频完整版.md` | set 去重与准入（同 dict 键规矩）、嵌套剥层（dict 方括号找键≠list 找位置）、列表推导式=for+append（实验等价）、Counter=dict 子类、词频完整版（isdigit 闸+双版对账）、报错词族 subscriptable | 2026-09-05 | 完成（正文誊自当日口答） |
| `python-遍历工具与成绩单分析.md` | enumerate/zip 职责与选型、zip 静默截断、嵌套 dict 聚合、同分并列"占号跳号"（same 计数器拉回组首）、预测→运行→修正、DoD 手算对照；三节补硬编码病根（科目名焊进变量名）、哨兵安全假设（None）、过期对照表＝裁判说谎 | 2026-09-05 | 完成（三/四节 2026-09-08 补填，誊自口答） |
| `python-函数默认值陷阱.md` | 默认值 def 时求值一次（`__defaults__` 为证）、None 哨兵＋体内新建、传参＝同对象双标签、收口公式"每次都要新的写进体内" | 2026-09-07 | 完成（四节本人已填） |
| `python-异常处理入门.md` | try/except 类型匹配、不接即停/接住续跑、`except Exception: pass` 吞错误、q 不进异常分支、前置校验 vs 异常处理 | 2026-09-07 | 完成（三节本人已填） |
| `python-作用域.md` | 编译时扫描整个函数体定局部名单、赋值前 print 也报 UnboundLocalError（格子预留但没值）、重贴标签要 global／改内容不用、避免 global＝写入点不可追踪 | 2026-09-07 | 完成（正文誊自本会话口答） |

> 注（2026-09-05 新增）：各笔记文件头已加 YAML frontmatter（id/created/topic/weakness_ids，静态元数据）；复习排程与状态见 `../review/queue.md`（唯一活跃真相源），弱点登记见 `../review/weaknesses.md`。