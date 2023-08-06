from . import Defines


def singular(word: str, *, path=()):
    mascul_neu_preset = {
        'р.п.': Defines.ask(word, path=path + ('мужской/средний род', 'родительный падеж')),
        'д.п.': Defines.ask(word, path=path + ('мужской/средний род', 'дательный падеж')),
        'т.п.': Defines.ask(word, path=path + ('мужской/средний род', 'творительный падеж')),
        'п.п.': Defines.ask(word, path=path + ('мужской/средний род', 'предложный падеж'))
    }

    mascul_preset = mascul_neu_preset.copy()
    mascul_preset[Defines.default] = '+'
    mascul_preset['в.п.'] = mascul_neu_preset['р.п.']

    neu_preset = mascul_neu_preset.copy()
    neu_preset[Defines.default] = Defines.ask(word, path=path + ('средний род', 'именительный/винительный падеж'))
    neu_preset['в.п.'] = neu_preset[Defines.default]

    fem_case = Defines.ask(word, path=path + ('женский род', 'родительный/дательный/творительный/предложный падеж'))

    return {
        Defines.default: mascul_preset,
        'с.р.': neu_preset,
        'ж.р.': {
            Defines.default: Defines.ask(word, path=path + ('женский род', 'именительный падеж')),
            'р.п.': fem_case,
            'д.п.': fem_case,
            'в.п.': Defines.ask(word, path=path + ('женский род', 'винительный падеж')),
            'т.п.': fem_case,
            'п.п.': fem_case
        }
    }

def plural(word: str, *, path=()):
    return {
        Defines.default: Defines.ask(word, path=path + ('именительный падеж', )),
        'р.п.': Defines.ask(word, path=path + ('родительный падеж', )),
        'д.п.': Defines.ask(word, path=path + ('дательный падеж', )),
        'в.п.': Defines.ask(word, path=path + ('винительный падеж', )),
        'т.п.': Defines.ask(word, path=path + ('творительный падеж', )),
        'п.п.': Defines.ask(word, path=path + ('предложный падеж', )),
    }