#cli_lab.py


"""
cli_lab.py — argparse 五段实验（T26 动手 · 修订版 2026-09-22）

本版对账栏已按 2026-09-22 实测填齐，退出码已用 $LASTEXITCODE 观测。

运行（PowerShell）：
  py -3.13 cli_lab.py exp1 --week W2 --top 3 --verbose; $LASTEXITCODE
  py -3.13 cli_lab.py exp1 --week W2;                   $LASTEXITCODE
  py -3.13 cli_lab.py exp1;                             $LASTEXITCODE
  py -3.13 cli_lab.py exp1 --help > help.txt            # 复核流

  py -3.13 cli_lab.py exp2 --b 2 --a 1;                 $LASTEXITCODE
  py -3.13 cli_lab.py exp2 --b abc --a 1;               $LASTEXITCODE

  py -3.13 cli_lab.py exp3;                             $LASTEXITCODE
  py -3.13 cli_lab.py exp3 raise --top -1;              $LASTEXITCODE
  py -3.13 cli_lab.py exp3 parser_error --top -1;       $LASTEXITCODE

  py -3.13 cli_lab.py exp4 --tags a b c
  py -3.13 cli_lab.py exp4 --tags
  py -3.13 cli_lab.py exp4 --mode
  py -3.13 cli_lab.py exp4 --mode-on
  py -3.13 cli_lab.py exp4 --bad-flag false
  py -3.13 cli_lab.py exp4 --good-flag false
  py -3.13 cli_lab.py exp4 --we W2
  py -3.13 cli_lab.py exp4 --w x;                       $LASTEXITCODE

  py -3.13 cli_lab.py exp5 plain;                       $LASTEXITCODE
  py -3.13 cli_lab.py exp5 required;                    $LASTEXITCODE
  py -3.13 cli_lab.py exp5 --verbose report --week W2
  py -3.13 cli_lab.py exp5 report --verbose --week W2;  $LASTEXITCODE

流验证：py -3.13 cli_lab.py exp1 --help > help.txt
        —— help.txt 有内容、屏幕无 error ⇒ --help 走 stdout 退 0。
"""

import argparse
import sys


# ============================================================
# 实验 1 — 声明即说明书
# ============================================================
def exp1():
    """
    预测（跑前写）：
      1. --help 输出走 stdout（不是 stderr），退出码 0。
      2. 不给 --week 时，两行走 stderr，原文逐字为：
           usage: cli_lab [-h] --week WEEK [--top TOP] [--verbose]
           cli_lab: error: the following arguments are required: --week
         退出码 2。
      3. vars(args) 是普通 dict（type 名 'dict'）。
      4. type(args).__name__ == 'Namespace'。

    对账（2026-09-22 实测）：
      - 正常给全：args = Namespace(week='W2', top=3, verbose=True)
                  type(args).__name__ = Namespace
                  vars(args) = {'week':'W2','top':3,'verbose':True}
                  type(vars(args)).__name__ = dict
                  退出码 0
      - 只给 --week：top=5（default 生效），verbose=False，退出码 0
      - 一个都不给：
          usage: cli_lab [-h] --week WEEK [--top TOP] [--verbose]
          cli_lab: error: the following arguments are required: --week
        退出码 2，走 stderr
      - --help：内容与用法行一致；重定向后 help.txt 有内容、屏幕干净，
                证实走 stdout、退出码 0（见文件头流验证）
      收口：我以为 --help 和 error 走同一条流；实际 help 走 stdout 退 0、
            error 走 stderr 退 2；因为 argparse 把 --help 当正常输出，
            只有错误才走 stderr 并统一退 2。
    """
    parser = argparse.ArgumentParser(prog="cli_lab")
    parser.add_argument("--week", required=True)
    parser.add_argument("--top", type=int, default=5)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    print("args =", args)
    print("type(args).__name__ =", type(args).__name__)
    print("vars(args) =", vars(args))
    print("type(vars(args)).__name__ =", type(vars(args)).__name__)


# ============================================================
# 实验 2 — 把"转换时机"变成看得见的东西（核心）
# ============================================================
def _trace_int(s):
    print("转换被调用：", s)
    return int(s)


def exp2():
    """
    预测（跑前写）：
      1. 两行"转换被调用"按【命令行出现顺序】出现：
           --b 2 --a 1  → 先 2，后 1
         不是按声明顺序（--a 声明在前，却后转）。
      2. --b abc --a 1：
           - 只打印 "转换被调用： abc"
           - --a 那行【不会】打印
         因为 --b 当场 int("abc") 失败，parse_args() 直接 usage+error 退出，
         根本不走到 --a。

    对账（2026-09-22 实测）：
      - py cli_lab.py exp2 --b 2 --a 1
          转换被调用： 2
          转换被调用： 1
          结果: 1 2
        退出码 0
      - py cli_lab.py exp2 --b abc --a 1
          转换被调用： abc
          usage: cli_lab [-h] [--a A] [--b B]
          cli_lab: error: argument --b: invalid _trace_int value: 'abc'
        退出码 2；--a 那行确实没出现
      收口：我以为 parse_args 可能先收齐再统一转；实际两行按命令行顺序出现、
            失败时根本不返回；因为转换就发生在匹配到该 token 的那一刻，
            业务代码永远看不到转坏的值。
    """
    parser = argparse.ArgumentParser(prog="cli_lab")
    parser.add_argument("--a", type=_trace_int)
    parser.add_argument("--b", type=_trace_int)
    args = parser.parse_args()
    print("结果:", args.a, args.b)


# ============================================================
# 实验 3 — 库的边界：default 和值域
# ============================================================
def exp3():
    """
    预测（跑前写）：
      ① type=int, default="5"，不传 --top：
         argparse 会把字符串 default 像命令行值一样应用 type
         → args.top 是 int 5（不是 '5'）。
      ② --top -1 语法层是合法 int，argparse 照收，不做值域。
      ③ 值域闸（top ≥ 1）两种收场：
         - raise ValueError → traceback 多行，stderr，退出码 1
         - parser.error()   → 一行 usage + 一行 error，stderr，退出码 2

    修法二选一（本次选 B）：
      A. parse_args(sys.argv[2:]) —— 自己让位。
         代价：argv 偏移在脚手架和业务之间手工对齐，加一层 subcommand
               又要重算，正是"顺序耦合"那族死法的新变体。
      B. add_argument("mode", nargs="?", choices=[...], default="default") —— 交给库。
         代价：多一个位置参数；好处是 choices 报错白送，
               非法 mode 直接退 2，不用自己 if。

    设计问题：
      parser.error() 要能用，parser 必须在拿得到的作用域里。
      - 方案 1：build_parser() 返回 parser，main(parser) 传进去。
        代价：多传一个对象；好处：错误收场走库统一口径（usage+exit 2）。
      - 方案 2：把值域做成 type= 函数。
        代价：type 函数里拿不到 parser，要么闭包、要么自己 raise
              ArgumentTypeError，报错措辞偏离库标准。
      （T27 接口 = NT(**vars(args))，在进契约前先拿到 parser。）

    对账（2026-09-22 实测）：
      ① py cli_lab.py exp3
           args.top = 5
           type(args.top) = <class 'int'>
         退出码 0。推翻笔记里"default 不走 type"那句。
      ② py cli_lab.py exp3 raise --top -1  → $LASTEXITCODE = 1
           Traceback (most recent call last):
             File "cli_lab.py", line 133, in exp3（行号系当时快照，现该句在 198 行）
               raise ValueError("top 必须 ≥ 1")
           ValueError: top 必须 ≥ 1
         多行 traceback，stderr
      ③ py cli_lab.py exp3 parser_error --top -1  → $LASTEXITCODE = 2
           usage: cli_lab [-h] [--top TOP] [{default,raise,parser_error}]
           cli_lab: error: --top 必须 ≥ 1
         一行 usage + 一行 error，stderr
      收口：我以为 default="5" 走不进 type；实际走进了、拿到 int；
            因为 argparse 把字符串默认值当"命令行缺席时的值"一样喂进 type，
            同一条规则换 "abc" 就炸成 invalid int value，措辞把程序 bug
            伪装成用户输入问题。
    """
    parser = argparse.ArgumentParser(prog="cli_lab")
    parser.add_argument(
        "mode",
        nargs="?",
        choices=["default", "raise", "parser_error"],
        default="default",
        help="default：只看 default 类型；raise/parser_error：走值域闸",
    )
    parser.add_argument("--top", type=int, default="5")
    args = parser.parse_args()

    if args.mode == "default":
        print("args.top =", args.top)
        print("type(args.top) =", type(args.top))
        return

    if args.mode == "raise":
        if args.top < 1:
            raise ValueError("top 必须 ≥ 1")
    elif args.mode == "parser_error":
        if args.top < 1:
            parser.error("--top 必须 ≥ 1")

    print("args.top =", args.top)


# ============================================================
# 实验 4 — nargs 三兄弟 + bool 陷阱 + 缩写
# ============================================================
def exp4():
    """
    预测（跑前写）：
      ① --tags nargs="+"：
           传 a b c      → ['a','b','c']
           一个不给       → None
           光杆 --tags    → 退 2，原文：
             cli_lab: error: argument --tags: expected at least one argument
      ② --mode nargs="?"：
           不配 const：--mode 单独 → None
           配 const="ON"：--mode-on 单独 → "ON"
      ③ type=bool 陷阱：
           --bad-flag false  → True
           --good-flag false → 退 2：unrecognized arguments: false
      ④ 缩写：
           --we W2 唯一命中 --week → 'W2'
           加了 --width 之后，--w x → 退 2：
             cli_lab: error: ambiguous option: --w could match --week, --width

    对账（2026-09-22 实测）：
      ① --tags a b c → ['a','b','c']；光杆 --tags 报错原文与预测逐字一致，
         退出码 2。
      ② --mode → None；--mode-on → ON；与预测一致，退出码 0。
      ③ --bad-flag false → True；--good-flag false → 退 2，
         原文 unrecognized arguments: false，退出码 2。
      ④ --we W2 → week='W2'（此时只有 --week，无歧义命中）；
         打开 --width 后，--w x 实测：
           usage: cli_lab [-h] [--tags TAGS [TAGS ...]] [--mode [MODE]]
                  [--mode-on [MODE_ON]] [--bad-flag BAD_FLAG] [--good-flag]
                  [--week WEEK] [--width WIDTH]
           cli_lab: error: ambiguous option: --w could match --week, --width
         退出码 2。
      收口：我以为 nargs="?" 不配 const 也能靠"给不给值"区分；实际不配
            时 --mode 就是 None、配 const="ON" 才拿到 "ON"；因为 nargs="?"
            必须配 const/default 才有意义，光有 ? 只是"值可省"。
    """
    parser = argparse.ArgumentParser(prog="cli_lab")
    parser.add_argument("--tags", nargs="+")
    parser.add_argument("--mode", nargs="?")                 # 无 const
    parser.add_argument("--mode-on", nargs="?", const="ON")  # 有 const
    parser.add_argument("--bad-flag", type=bool)
    parser.add_argument("--good-flag", action="store_true")
    parser.add_argument("--week")
    parser.add_argument("--width")   # 打开，让 --w 歧义
    args = parser.parse_args()
    print("tags      =", args.tags)
    print("mode      =", args.mode)
    print("mode_on   =", args.mode_on)
    print("bad_flag  =", args.bad_flag)
    print("good_flag =", args.good_flag)
    print("week      =", args.week)
    print("width     =", args.width)


# ============================================================
# 实验 5 — subcommand（git commit 那种结构）
# ============================================================
def exp5():
    """
    预测（跑前写）：
      ① plain（不写 dest、不写 required），不给子命令：
           不报错，退 0，Namespace(verbose=False)；
           访问 args.cmd → AttributeError:
             'Namespace' object has no attribute 'cmd'
      ② required（required=True，不写 dest），不给子命令：
           退 2，原文：
             cli_lab: error: the following arguments are required: {report,export}
      ③ 全局 --verbose：
           放子命令【前】合法：--verbose report --week W2
           放子命令【后】不合法：report --verbose --week W2 → 退 2

    脚手架约定：第一个 token 是 plain / required 时用来选变体；
    其余交给 argparse。sub 是默认变体（带 dest="cmd"）。

    对账（2026-09-22 实测）：
      ① py cli_lab.py exp5 plain  → $LASTEXITCODE = 1
           args = Namespace(verbose=False)
           Traceback (most recent call last):
             File "cli_lab.py", line 245, in exp5（行号系当时快照，现该句在 329 行）
               print("args.cmd =", args.cmd)
           AttributeError: 'Namespace' object has no attribute 'cmd'
         不写 dest 时 Namespace 里真没 cmd；错名是 AttributeError（不是 KeyError）。
      ② py cli_lab.py exp5 required  → $LASTEXITCODE = 2
           usage: cli_lab [-h] [--verbose] {report,export} ...
           cli_lab: error: the following arguments are required: {report,export}
      ③ --verbose report --week W2  → Namespace(verbose=True, cmd='report', week='W2')
         report --verbose --week W2  → 退 2：unrecognized arguments: --verbose
      收口：我以为"不给子命令"会报错；实际 plain 态静静返回、访问 args.cmd
            才撞 AttributeError；因为 add_subparsers() 默认不强制，要必填
            得显式 required=True。上一轮三枪同果是因为两行注释没真打开——
            "多份证据同果"本身就是"我没真的改到"的信号。
    """
    if len(sys.argv) > 1 and sys.argv[1] in ("plain", "required"):
        variant = sys.argv[1]
        argv = sys.argv[2:]
    else:
        variant = "sub"
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(prog="cli_lab")
    parser.add_argument("--verbose", action="store_true")

    if variant == "plain":
        sub = parser.add_subparsers()
    elif variant == "required":
        sub = parser.add_subparsers(required=True)
    else:  # sub
        sub = parser.add_subparsers(dest="cmd")

    p_report = sub.add_parser("report")
    p_report.add_argument("--week")

    p_export = sub.add_parser("export")
    p_export.add_argument("--format")

    args = parser.parse_args(argv)
    print("args =", args)

    if variant == "plain":
        # 故意访问 args.cmd：没写 dest 时 Namespace 里没有这个属性
        print("args.cmd =", args.cmd)


# ============================================================
# 分发
# ============================================================
DISPATCH = {
    "exp1": exp1,
    "exp2": exp2,
    "exp3": exp3,
    "exp4": exp4,
    "exp5": exp5,
}


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in DISPATCH:
        print(
            f"用法: python {sys.argv[0]} <{'|'.join(DISPATCH)}> [其他参数...]",
            file=sys.stderr,
        )
        sys.exit(2)
    which = sys.argv[1]
    # 剥掉 "expN"，让每个实验内部拿到的 sys.argv 跟单独脚本一样
    sys.argv = [sys.argv[0]] + sys.argv[2:]
    DISPATCH[which]()