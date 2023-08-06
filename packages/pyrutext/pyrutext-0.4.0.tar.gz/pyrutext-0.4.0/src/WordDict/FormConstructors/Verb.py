from . import Defines


def imperative(word: str, *, path=()):
    imperative_form = Defines.ask(word, path)
    return {
        Defines.default: imperative_form,
        'мн.ч.': imperative_form + 'те'
    }

def conjugable(word: str, *args, path=()):
    forms = {}

    forms[Defines.default] = '+'
    forms['п.в.'] = time_past(word, path=path + ('Прошедшее время', ))
    forms['б.в.'] = time(word, *args, 'б.в.', path=path + ('Будущее время', ))
    if 'несов.' in args:
        forms['н.в.'] = time(word, *args, 'н.в.', path=path + ('Настоящее время', ))

    return forms

def time_past(word: str, *, path=()):
    forms = {}

    standard_form = Defines.ask(word, path)

    forms[Defines.default] = standard_form  # мужской род
    if standard_form[-1] != 'л':
        standard_form = standard_form + 'л'
    forms['ж.р.'] = standard_form + 'а'
    forms['с.р.'] = standard_form + 'о'
    forms['мн.ч.'] = standard_form + 'и'

    return forms

def time(word: str, *args, path=()):
    return {
        Defines.default: '+',
        '1л': person(word, *args, '1л', path=path + ('первое лицо', )),
        '2л': person(word, *args, '2л', path=path + ('второе лицо', )),
        '3л': person(word, *args, '3л', path=path + ('третье лицо', ))
    }

def person(word: str, *args, path=()):
    if 'б.в.' in args and 'несов.' in args:
        return {
            Defines.default: 'буду +',
            'мн.ч.': 'будем +'
        } if '1л' in args else {
            Defines.default: 'будешь +',
            'мн.ч.': 'будете +'
        } if '2л' in args else {
            Defines.default: 'будет +',
            'мн.ч.': 'будут +'
        }

    return {
        Defines.default: Defines.ask(word, path=path + ('единственное число', )),
        'мн.ч.': Defines.ask(word, path=path + ('множественное число', ))
    }