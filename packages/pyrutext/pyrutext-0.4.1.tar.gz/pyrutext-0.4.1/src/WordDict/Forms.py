from .FormConstructors import Adj, Noun, Verb, Defines


def lookup(self, *args):
    if type(self) is not dict:
        return self

    default_key = Defines.default if Defines.default_key not in self else self[Defines.default_key]

    for key, value in self.items():
        if key in args:
            return lookup(value, *args)

    value = self[default_key]
    return lookup(value, *args)


def construct_forms(word: str, *args, path=()):
    if 'гл.' in args:
        return {
            Defines.default: Verb.conjugable(word, *args, path=path),
            'пов.': Verb.imperative(word, path=path + ('Повелительное наклонение', )),
            'инф.': '+'
        }
    elif 'сущ.' in args:
        return '+' if 'нескл.' in args else Noun.declined(word, *args, path=path)
    elif 'пр.' in args:
        return {
            Defines.default: Adj.singular(word, path=path + ('Единственное число', )),
            'мн.ч.': Adj.plural(word, path=path + ('Множественное число', ))
        }
    else:
        return '+'