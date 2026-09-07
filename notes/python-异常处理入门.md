---
id: N008
title: 异常处理入门
created: 2026-09-07
topic: python-basics
weakness_ids: [WK005]
---

# W3 预习：异常处理入门（2026-09-07）

> 起草：AI ｜ 内容确认：OZONGO
> 分工：**零节清单与脚手架由 AI 起草**；一/二节＝AI 誊自本人口答（未加问答之外内容）；**三节待本人填写**。
> 关联：`../python-100/w3/try_except.py`（本课实验）、`../python-100/w2/contacts.py`（try/except 改造验收）、`python-输入校验与字符串陷阱.md`（isdigit 前置校验＝LBYL 同族）、`python-函数默认值陷阱.md`（同日另一课）

---

## 零、待复述问题清单（AI 起草）

> **用法**：合上代码、合上本文，逐题作答。答不上来的那题，就是你以为会了其实没会的地方。
> 通关标准：5 题至少 4 题能**脱稿说清**，第 2、3 题必说清。

1. `try/except` 的结构里，什么时候正常执行？什么时候跳到 `except`？
2. `except ValueError:` 为什么接不住 `KeyError`？一句话说出机制。
3. `except Exception: pass` 为什么危险？它会把什么变成沉默型 bug？
4. 通讯录菜单里 `q` 为什么应该先判断，而不是靠 `int("q")` 报错来处理？
5. 什么时候用前置校验（如 `isdigit`、`in`、空值判断）？什么时候用异常处理更合适？

---

## 一、课堂实验与口答（AI 誊自本人口答）

### Q1：未捕获异常会中断后续语句

```python
print("A")
int("abc")
print("B")
```

- **本人口答**：`不会被打印，会报错int("abc")`；补充：**`ValueError`**。
- **收口**：屏幕顺序是 `A` → `ValueError` traceback → 不会打印 `B`。

### Q2：except 接住 ValueError 后继续执行

```python
try:
    x = int("abc")
except ValueError:
    x = 0
print(x)
```

- **本人口答**：`0吗？`
- **实际输出**：`0`

### Q3：异常类型不匹配时，except 不处理

```python
try:
    d = {"a": 1}
    print(d["b"])
except ValueError:
    print("数字不对")
print("done")
```

- **本人口答**：`三个字符串都不会输出，因为d["b"]没有键"b"所以KeyError，所以except ValueError:不会执行`
- **实际报错末行**：`KeyError: 'b'`

### Q4：改成 `except KeyError` 后能接住

- **本人口答预测**：`第一行 数字不对 / 第二行 done`
- **实际输出**：`数字不对 / done`
- **AI 点破**：`except` 只接匹配类型；匹配后从 `try/except` 块之后继续执行，所以会打印 `done`。

### Q5：`except Exception: pass` 会吞掉错误

```python
try:
    d = {"a": 1}
    print(d["b"])
except Exception:
    pass
print("done")
```

- **本人口答**：`会看到done`；`没多什么，少了print("数字不对")`
- **实际输出**：`done`
- **收口**：不匹配异常＝不接＝程序停；匹配异常＝接住＝继续往后走；`except Exception: pass`＝真实错误被藏掉。

---

## 二、contacts.py 改造结论（AI 誊自课堂）

- `q` 是正常菜单选项，不应依赖 `int(t)` 报错退出；应放在 `try` 之前先判断并 `break`。
- `try/except ValueError` 适合包住“输入不是整数”的异常路径；但业务状态不要塞进异常分支。
- `except Exception: pass` 只能用于故意静默；学习项目默认不要用，至少 `print` 留证据。

---

## 三、本人填写

q 是用户正常退出意图，不是异常；应该先判断 `t == "q"` 并 `break`，而不是让 `int("q")` 抛 `ValueError` 后再靠 `except` 收拾。
