default = '_def'
default_key = '_defkey'
tags_key = '_tags'

def ask(word: str, path=()):
    print(path[0], end='')
    for dir in path[1:]:
        print(f', {dir}', end='')
    print(f' для слова "{word}": ', end='')
    return input()