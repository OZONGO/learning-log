#接收提示语名称
#输入＋验证＋重问直到合法
#返回合法输入转换的浮点数

def num_check(name: str) -> float:
    """通用数字输入验证函数，name 为提示名称（如'摄氏度'）"""
    while True:
        inp = input(f"请输入{name}: ")
        # 检查负号和小数点个数（合法：最多一个负号且必须在开头，最多一个小数点）
        if inp.count("-") > 1 or inp.count(".") > 1:
            print(f"请输入有效{name}")
            continue
        # 去掉一个负号和一个点后检查剩余字符是否为数字
        checked = inp.replace(".", "", 1).replace("-", "", 1)
        if not checked.isdigit():
            print(f"请输入有效{name}")
            continue
        # 若有一个负号但不在开头，非法
        if inp.count("-") == 1 and not inp.startswith("-"):
            print(f"请输入有效{name}")
            continue
        value = float(inp)
        return value
    
if __name__ == "__main__":
    print("被直接运行")