class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def colorize_rust_code(code):
    code = code.replace(
        'println!("', f'{Colors.GREEN}println!{Colors.END}{Colors.BLUE}("')
    code = code.replace('",', f'",{Colors.END}')

    words = code.split(" ")
    colorized_words = [colorize_individual_word(word) for word in words]
    return " ".join(colorized_words)


def colorize_individual_word(word):
    word = colorize_keywords(word)
    word = colorize_types(word)
    return word


def colorize_keywords(word):
    keywords = ['fn', 'struct', 'impl', 'match', 'for', 'in', 'return']
    if word in keywords:
        return f'{Colors.GREEN}{word}{Colors.END}'
    return word


def colorize_types(word):
    types = ['i32', 'f32', 'String', 'bool', 'Result', 'Option']
    if word in types:
        return f'{Colors.YELLOW}{word}{Colors.END}'
    return word


def colorize_string_literals(code):
    return code.replace('"', f'{Colors.BLUE}"')
