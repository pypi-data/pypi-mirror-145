from . import Defines


def declined(word: str, *args, path=()):
    return {
        Defines.default: case(word, *args, 'и.п.', path=path + ('Именительный падеж', )),
        'р.п.': case(word, *args, 'р.п.', path=path + ('Родительный падеж', )),
        'д.п.': case(word, *args, 'д.п.', path=path + ('Дательный падеж', )),
        'в.п.': case(word, *args, 'в.п.', path=path + ('Винительный падеж', )),
        'т.п.': case(word, *args, 'т.п.', path=path + ('Творительный падеж', )),
        'п.п.': case(word, *args, 'п.п.', path=path + ('Предложный падеж', ))
    }

def case(word: str, *args, path=()):
    return {
        Defines.default: '+' if 'и.п.' in args else Defines.ask(word, path)
    } if 'ед.ч.' in args or 'мн.ч.' in args else {
        Defines.default: '+' if 'и.п.' in args else Defines.ask(word, path + ('единственное число', )),
        'мн.ч.': Defines.ask(word, path + ('множественное число', ))
    }