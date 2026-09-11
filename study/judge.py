# -*- coding: utf-8 -*-
"""
力扣式自动判题脚本（混合模式学习助手）

用法:
    python judge.py <题目文件.md> <解法文件.py>

示例:
    python judge.py problems/两数之和.md records/我的解法.py

解法文件支持两种写法:

1. solve() 函数式（推荐）:
       def solve(nums, target):
           return [0, 1]
   题目文件里的每个用例的 input 会按顺序拆开传给 solve，
   返回值与 expected 比对。

2. 标准输入输出式:
   你的脚本从 input() 读数据、用 print() 输出，
   题目用例的 input 原文作为标准输入喂给你的脚本，比对标准输出。
"""

import copy
import importlib.util
import json
import re
import subprocess
import sys
import threading
from pathlib import Path

TIMEOUT = 5  # 单个用例限时（秒）


# ── 链表题支持：题目用例声明 "convert": "linkedlist" 时启用 ──
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def to_linkedlist(lst):
    """列表 → 链表，返回头结点（空列表返回 None；非列表参数原样返回，支持 [链表, n] 这类多参数题）"""
    if not isinstance(lst, list):
        return lst
    dummy = ListNode()
    tail = dummy
    for v in lst:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def to_list(node):
    """链表 → 列表"""
    out = []
    while node is not None:
        out.append(node.val)
        node = node.next
    return out


def load_problem(path):
    """从题目 Markdown 里解析题面和 JSON 测试用例块。"""
    text = Path(path).read_text(encoding="utf-8")
    title_m = re.match(r"#\s*(.+)", text)
    title = title_m.group(1).strip() if title_m else Path(path).stem

    m = re.search(r"```json\s*\n(.*?)```", text, re.S)
    if not m:
        print(f"错误: 题目文件里没有找到 ```json 测试用例块: {path}")
        sys.exit(1)
    try:
        tests = json.loads(m.group(1))
    except json.JSONDecodeError as e:
        print(f"错误: 测试用例 JSON 格式不对: {e}")
        sys.exit(1)
    return title, tests


def load_solution(path):
    """加载解法文件，返回 (solve函数或None, 文件路径)。"""
    mod_name = "solution_" + Path(path).stem
    spec = importlib.util.spec_from_file_location(mod_name, path)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except SystemExit:
        pass  # 解法里写了 sys.exit 也不影响
    except Exception as e:
        print(f"错误: 解法文件加载失败: {type(e).__name__}: {e}")
        sys.exit(1)
    mod.ListNode = ListNode  # 链表题解法需要 ListNode，由判题器注入
    solve = getattr(mod, "solve", None)
    if solve is None and hasattr(mod, "Solution"):
        # 支持力扣的 class Solution 写法：取类里唯一的公开方法
        methods = [f for f in vars(mod.Solution).values()
                   if callable(f) and not f.__name__.startswith("_")
                   and getattr(f, "__qualname__", "").startswith("Solution")]
        if len(methods) == 1:
            # 绑定到实例上，避免调用时缺 self
            solve = getattr(mod.Solution(), methods[0].__name__)
        elif len(methods) > 1:
            print("提示: Solution 里有多个方法，请在文件里另写一个 solve() 供判题调用")
    return solve


def run_with_timeout(fn, timeout):
    """带超时地调用 fn()，返回 (结果, 是否超时, 异常或None)。"""
    box = {}

    def target():
        try:
            box["result"] = fn()
        except Exception as e:
            box["error"] = e

    t = threading.Thread(target=target, daemon=True)
    t.start()
    t.join(timeout)
    if t.is_alive():
        return None, True, None
    if "error" in box:
        return None, False, box["error"]
    return box.get("result"), False, None


def normalize(value):
    """统一序列化后再比对，容忍 1 vs 1.0、元组 vs 列表等差异。"""
    try:
        return json.dumps(value, sort_keys=True, ensure_ascii=False)
    except (TypeError, ValueError):
        return str(value)


def main():
    # Windows GBK 终端打印 emoji 会崩，统一转 UTF-8
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    title, tests = load_problem(sys.argv[1])
    solve = load_solution(sys.argv[2])

    print(f"题目: {title}")
    print(f"用例数: {len(tests)}")
    print("-" * 46)

    passed = 0
    for i, case in enumerate(tests, 1):
        inp, expected = case["input"], case["expected"]
        convert = case.get("convert")
        shown_input = copy.deepcopy(inp)  # 快照：原地修改型解法会改掉 inp，展示要用原件

        if solve is not None:
            args = inp if isinstance(inp, list) else [inp]
            if convert == "linkedlist":
                args = [to_linkedlist(a) for a in args]
            actual, timed_out, err = run_with_timeout(
                lambda: solve(*args), TIMEOUT)
            if convert == "linkedlist":
                # 链表题返回 None 等价于空链表
                actual = [] if actual is None else to_list(actual)
            elif convert == "array_mutate":
                # 原地修改数组题：期望 [返回值k, 数组前k位]
                k = actual if isinstance(actual, int) else -1
                first = args[0] if args else []
                actual = [k, list(first[:max(k, 0)])]
            elif convert == "array_inplace":
                # 原地修改且无返回值的题（如移动零）：只验证数组的最终状态
                actual = list(args[0]) if args else []
        else:
            # 标准输入输出模式
            try:
                p = subprocess.run(
                    [sys.executable, sys.argv[2]],
                    input=str(inp), capture_output=True, text=True,
                    encoding="utf-8", timeout=TIMEOUT)
            except subprocess.TimeoutExpired:
                print(f"❌ 用例{i} 超时 (> {TIMEOUT}s)")
                continue
            if p.returncode != 0:
                print(f"❌ 用例{i} 运行出错:\n{p.stderr.strip()}")
                continue
            actual, timed_out, err = p.stdout, False, None

        if timed_out:
            print(f"❌ 用例{i} 超时 (> {TIMEOUT}s)")
            continue
        if err is not None:
            print(f"❌ 用例{i} 抛出异常: {type(err).__name__}: {err}")
            continue

        if normalize(actual) == normalize(expected):
            passed += 1
            print(f"✅ 用例{i} 通过")
        else:
            print(f"❌ 用例{i} 失败")
            print(f"   输入: {shown_input!r}")
            print(f"   期望: {expected!r}")
            print(f"   实际: {actual!r}")

    print("-" * 46)
    print(f"结果: {passed}/{len(tests)} 通过")
    if passed == len(tests):
        print("🎉 全部通过！把代码发给我做点评吧。")
    else:
        print("还有用例没过，检查一下边界条件，或者把代码发给我一起看。")
    sys.exit(0 if passed == len(tests) else 1)


if __name__ == "__main__":
    main()
