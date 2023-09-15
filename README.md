![Python Version](https://img.shields.io/badge/python-3.11.4-blue)


`rusthon` is a minimalist transpilation tool that converts a subset of the Python language to Rust. Designed to help developers grasp the basic concepts of transpilation, Rusthon provides a direct translation of common Python constructs to their Rust counterparts.

## Feature
Currently, Rusthon supports the transpilation of the following constructs:

- Functions with typed arguments and a typed return.
- Basic arithmetic operations (+, -, *, /).
- Function calls.
- Variable assignments.
- The conditional declaration if __name__ == "__main__":.
- The print() function.
- For loop and range()

## How to Use
1. Clone the repository:
```
git clone https://github.com/urso-ai/rusthon.git
cd rusthon
```
2. Place your Python code in the `test_sample.py` file.
3. Run `main.py`:
```
python main.py
```
4. The resulting Rust code will be diplayed on the standard output.

## Limitations
Rusthon is a teaching tool designed to transpile a specific subset of Python. As such, many Python language constructs, such as loops, classes, and exception handling, are not yet supported. Contributions to expand functionality are welcome!

## Contributing
If you'd like to contribute to the project, feel free to fork and send a pull request. Any feedback or suggestions are appreciated!

## License
MIT
