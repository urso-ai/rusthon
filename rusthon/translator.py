import ast

known_classes = set()


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

    elif isinstance(node, ast.For):
        return translate_for(node)

    elif isinstance(node, ast.Call):
        return translate_call(node)

    elif isinstance(node, ast.Attribute):
        return f"{translate_node(node.value)}.{node.attr}"

    elif isinstance(node, ast.ClassDef):
        return translate_class(node)

    elif isinstance(node, ast.Constant):
        if isinstance(node.value, str):
            return f'"{node.value}"'
        else:
            return str(node.value)

    elif isinstance(node, ast.Try):
        return translate_try_except(node)

    elif isinstance(node, ast.Import):
        return translate_import(node)

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
    if isinstance(node.func, ast.Name) and node.func.id == "range":
        if len(node.args) == 1:
            stop_value = translate_node(node.args[0])
            return f"0..{stop_value}"
        elif len(node.args) == 2:
            start_value = translate_node(node.args[0])
            stop_value = translate_node(node.args[1])
            return f"{start_value}..{stop_value}"
        else:
            return f"/* Rusthon: unsupported range arguments. */"

    if isinstance(node.func, ast.Name) and node.func.id in known_classes:
        args = ', '.join([translate_node(arg) for arg in node.args])
        return f"{node.func.id}::new({args})"

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


def translate_for(node):
    if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name) and node.iter.func.id == "range":
        target = translate_node(node.target)
        if len(node.iter.args) == 1:
            loop_range = translate_call(node.iter)
            loop_body = "\n    ".join([translate_node(stmt)
                                      for stmt in node.body])
            return f"for {target} in {loop_range} {{\n    {loop_body}\n}}"
        elif len(node.iter.args) == 2:
            loop_range = translate_call(node.iter)
            loop_body = "\n    ".join([translate_node(stmt)
                                      for stmt in node.body])
            return f"for {target} in {loop_range} {{\n    {loop_body}\n}}"
        else:
            return f"/* Rusthon: unsupported range arguments in for loop. */"
    else:
        return f"/* Rusthon: unsupported loop type. */"


def translate_class(node):
    class_name = node.name
    fields = []
    known_classes.add(class_name)

    for item in node.body:
        if isinstance(item, ast.FunctionDef) and item.name == "__init__":
            for arg in item.args.args:
                if arg.arg != 'self':
                    fields.append((arg.arg, translate_type(arg.annotation)))

    fields_str = ",\n    ".join([f"{name}: {type_}" for name, type_ in fields])
    struct_str = f"struct {class_name} {{\n    {fields_str}\n}}\n\n"

    args_str = ", ".join([f"{name}: {type_}" for name, type_ in fields])
    impl_str = f"impl {class_name} {{\n    fn new({args_str}) -> {class_name} {{\n        {class_name} {{ {', '.join([name for name, _ in fields])} }}\n    }}\n}}\n\n"

    return struct_str + impl_str


def translate_type_from_value(node):
    if isinstance(node, ast.Str):
        return "String"
    elif isinstance(node, ast.Num):
        if isinstance(node.n, int):
            return "i32"
        elif isinstance(node.n, float):
            return "f32"
    elif isinstance(node, ast.NameConstant) and node.value is None:
        return "Option"
    return "unknown_type"


def translate_import(node):
    return f"// TODO: Handle import {', '.join([alias.name for alias in node.names])}"


def translate_try_except(node):
    try_body = "\n    ".join([translate_node(stmt) for stmt in node.body])
    except_body = "\n    ".join([translate_node(stmt)
                                for stmt in node.handlers[0].body])

    return f"match (|| -> Result<_, &'static str> {{\n    {try_body}\n    Ok(())\n}})() {{\n    Ok(_) => {{ {try_body} }},\n    Err(e) => {{ {except_body} }}\n}}"
