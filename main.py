from rusthon.translator import translate_node
from rusthon.utils import analyze_python_code


def main():
    with open('tests/test_sample.py', 'r') as file:
        python_code = file.read()

    ast_tree = analyze_python_code(python_code)

    if ast_tree:
        rust_code = "\n".join([translate_node(stmt) for stmt in ast_tree.body])
    else:
        rust_code = "Error parsing the Python code."

    print("Generated Rust code:")
    print("====================")
    print(rust_code)


if __name__ == "__main__":
    main()
