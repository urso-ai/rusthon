import ast


def analyze_python_code(code):
    try:
        tree = ast.parse(code)
        return tree
    except Exception as e:
        return None
