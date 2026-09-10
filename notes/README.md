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
| `python-可变参数.md` | def 处打包（位置→tuple／关键字→dict）vs 调用处解包（倒货不补货）、磁铁松严格、报错术语跟 def 身份表走（positional／keyword-only、* 是分界线）、args 是 tuple、硬编码病根＝焊进变量名 | 2026-09-08 | 完成（正文誊自本会话口答） |
| `python-模块与import.md` | 模块=.py；import 只执行顶层（def 挂名不跑体）；import 整模块 vs from 取一名的选型；`__name__` 双面孔守卫；同名遮蔽标准库；`__pycache__`＝执行痕迹；numcheck 输入助手版重构（领域规则留调用方、`.5` 洞保留） | 2026-09-09 | 完成（正文誊自本会话口答） |
| `python-异常抛出与文件读写.md` | raise＝不可能被忽略／预期内错→重问、程序 bug→raise；r-w-x 三模式"第一次动作"时刻表（w 在 open 那一刻截断、不可逆）；with 保证 `__exit__`＝无论怎么出去都关；文本层与字节层是两套现实（`\n`→`\r\n`、删 encoding≠关翻译而是退回 GBK）；文件对象是带位置的游标不是容器；JSON 键只能是字符串、`ensure_ascii=False`；**traceback 真凶定位规则升级**（终端 vs F5 帧顺序相反→"离异常类型最近的 File 行"）；救援路径不能依赖被救对象是好的；"跑对了但原因是假的"两次现场 | 2026-09-10 | 完成（正文誊自本会话口答；四节待填） |

> 注（2026-09-05 新增）：各笔记文件头已加 YAML frontmatter（id/created/topic/weakness_ids，静态元数据）；复习排程与状态见 `../review/queue.md`（唯一活跃真相源），弱点登记见 `../review/weaknesses.md`。