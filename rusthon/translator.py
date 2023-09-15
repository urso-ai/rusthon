import ast


def translate_node(node):
    if isinstance(node, ast.BinOp):
        ops = {
            ast.Add: "+",
            ast.Sub: "-",
            ast.Mult: "*",
            ast.Div: "/"
        }
        return f"{translate_node(node.left)} {ops[type(node.op)]} {translate_node(node.right)}"

    elif isinstance(node, ast.Assign):
        targets = ' '.join([translate_node(target) for target in node.targets])
        value = translate_node(node.value)
        return f"{targets} = {value};"

    elif isinstance(node, ast.Name):
        return node.id

    elif isinstance(node, ast.Num):
        return str(node.n)

    elif isinstance(node, ast.FunctionDef):
        return translate_function(node)

    elif isinstance(node, ast.If):
        return translate_if(node)

    elif isinstance(node, ast.Return):
        return translate_return(node)

    elif isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name) and node.func.id == "print":
            return translate_print(node)
        return translate_call(node)

    elif isinstance(node, ast.Expr):
        return translate_node(node.value) + ";"

    return f"/* Rusthon: unable to translate the segment. ({type(node).__name__}) */"


def translate_function(node):
    func_name = node.name
    args = ', '.join(
        [f"{arg.arg}: {translate_type(arg.annotation)}" for arg in node.args.args])
    return_type = translate_type(node.returns)

    body = "\n    ".join([translate_node(stmt) for stmt in node.body])

    return f"fn {func_name}({args}) -> {return_type} {{\n    {body}\n}}\n\n"


def translate_type(node):
    if isinstance(node, ast.Name):
        types_map = {
            "int": "i32",
            "float": "f32",
            "str": "String",
            "bool": "bool"
        }
        return types_map.get(node.id, "unknown_type")
    return "unknown_type"


def translate_call(node):
    func_name = translate_node(node.func)
    args = ', '.join([translate_node(arg) for arg in node.args])
    return f"{func_name}({args})"


def translate_if(node):
    if (isinstance(node.test, ast.Compare) and
        isinstance(node.test.left, ast.Name) and
        node.test.left.id == "__name__" and
        isinstance(node.test.comparators[0], ast.Str) and
            node.test.comparators[0].s == "__main__"):

        body = "\n    ".join([translate_node(stmt) for stmt in node.body])
        return f"fn main() {{\n    {body}\n}}\n\n"
    else:
        return f"/* Rusthon: unable to translate the segment. */"


def translate_print(node):
    args_count = len(node.args)
    placeholders = ", ".join(["{}" for _ in range(args_count)])
    args_translated = ", ".join([translate_node(arg) for arg in node.args])
    return f'println!("{placeholders}", {args_translated});'


def translate_return(node):
    return_expr = translate_node(node.value)
    return f"return {return_expr};"
