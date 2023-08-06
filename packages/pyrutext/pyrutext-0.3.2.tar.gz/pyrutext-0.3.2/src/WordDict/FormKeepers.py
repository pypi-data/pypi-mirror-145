_default = '_def'
_default_key = '_defkey'


class FormKeeper():
    def __init__(self):
        global _default
        self.rooms = {}
        self.default_key = _default

    def ask(self, word: str, path=()):
        print(path[0], end='')
        for dir in path[1:]:
            print(f', {dir}', end='')
        print(f' для слова "{word}": ', end='')
        return input()

    def accept(self, *args):
        for key, value in self.rooms.items():
            if key in args:
                if type(value) is str:
                    return value
                return value.accept(*args)

        value = self.rooms[self.default_key]
        if type(value) is str:
            return value
        return value.accept(*args)

    def to_dict(self):
        global _default
        global _default_key
        to_return = {}

        if self.default_key != _default:
            to_return[_default_key] = self.default_key

        for key, value in self.rooms.items():
            if type(value) is str:
                to_return[key] = value
            else:
                to_return[key] = value.to_dict()

        return to_return


class CustomFormKeeper(FormKeeper):
    def __init__(self, forms={}):
        global _default_key
        super().__init__()

        if _default_key in forms:
            self.default_key = forms[_default_key]
            del forms[_default_key]

        for key, value in forms.items():
            if type(value) is str:
                self.rooms[key] = value
            else:
                self.rooms[key] = CustomFormKeeper(value)


class BaseFormKeeper(FormKeeper):
    def __init__(self, word: str, *args, path=()):
        super().__init__()

        if 'гл.' in args:
            self.rooms['инф.'] = '+'
            self.rooms['пов.'] = VerbImperativeFormKeeper(word, path=path + ('Повелительное наклонение', ))
            self.rooms[self.default_key] = VerbConjugableFormKeeper(word, *args, path=path)
        elif 'сущ.' in args:
            if 'нескл.' in args:
                self.rooms[self.default_key] = '+'
            else:
                self.rooms[self.default_key] = NounDeclinedFormKeeper(word, *args, path=path)
        elif 'пр.' in args:
            self.default_key = 'ед.ч.'
            self.rooms['ед.ч.'] = AdjSingularFormKeeper(word, *args, path=path + ('Единственное число', ))
            self.rooms['мн.ч.'] = AdjCaseFormKeeper(word, *args, path=path + ('Множественное число', ))
        else:
            self.rooms[self.default_key] = '+'


class VerbImperativeFormKeeper(FormKeeper):
    def __init__(self, word: str, *, path=()):
        super().__init__()

        imperative_form = self.ask(word, path, )
        self.rooms[self.default_key] = imperative_form
        self.rooms['мн.ч.'] = imperative_form + 'те'


class VerbConjugableFormKeeper(FormKeeper):
    def __init__(self, word: str, *args, path=()):
        super().__init__()

        self.rooms[self.default_key] = '+'

        self.rooms['п.в.'] = VerbPastTimeFormKeeper(word, path=path + ('Прошедшее время', ))
        self.rooms['б.в.'] = VerbTimeFormKeeper(word, *args, path=path + ('Будущее время', ))
        if 'несов.' in args:
            self.rooms['н.в.'] = VerbTimeFormKeeper(word, *args, path=path + ('Настоящее время', ))


class VerbPastTimeFormKeeper(FormKeeper):
    def __init__(self, word: str, *, path=()):
        super().__init__()

        standard_form = self.ask(word, path)
        self.default_key = 'м.р.'

        self.rooms['м.р.'] = standard_form
        if standard_form[-1] != 'л':
            standard_form = standard_form + 'л'
        self.rooms['ж.р.'] = standard_form + 'а'
        self.rooms['с.р.'] = standard_form + 'о'
        self.rooms['мн.ч.'] = standard_form + 'и'


class VerbTimeFormKeeper(FormKeeper):
    def __init__(self, word: str, *args, path=()):
        super().__init__()

        self.rooms[self.default_key] = '+'

        self.rooms['1л'] = VerbPersonFormKeeper(word, *args, path=path + ('первое лицо', ))
        self.rooms['2л'] = VerbPersonFormKeeper(word, *args, path=path + ('второе лицо', ))
        self.rooms['3л'] = VerbPersonFormKeeper(word, *args, path=path + ('третье лицо', ))


class VerbPersonFormKeeper(FormKeeper):
    def __init__(self, word: str, *args, path=()):
        super().__init__()

        self.default_key = 'ед.ч.'

        if 'несов.' in args and 'Будущее время' in path:
            if 'первое лицо' in path:
                self.rooms['ед.ч.'] = 'буду +'
                self.rooms['мн.ч.'] = 'будем +'
                return
            if 'второе лицо' in path:
                self.rooms['ед.ч.'] = 'будешь +'
                self.rooms['мн.ч.'] = 'будете +'
                return
            if 'третье лицо' in path:
                self.rooms['ед.ч.'] = 'будет +'
                self.rooms['мн.ч.'] = 'будут +'
                return

        self.rooms['ед.ч.'] = self.ask(word, path + ('единственное число', ))
        self.rooms['мн.ч.'] = self.ask(word, path + ('множественное число', ))


class NounDeclinedFormKeeper(FormKeeper):
    def __init__(self, word: str, *args, path=()):
        super().__init__()

        self.default_key = 'и.п.'

        self.rooms['и.п.'] = NounCaseFormKeeper(word, *args, path=path + ('Именительный падеж', ))
        self.rooms['р.п.'] = NounCaseFormKeeper(word, *args, path=path + ('Родительный падеж', ))
        self.rooms['д.п.'] = NounCaseFormKeeper(word, *args, path=path + ('Дательный падеж', ))
        self.rooms['в.п.'] = NounCaseFormKeeper(word, *args, path=path + ('Винительный падеж', ))
        self.rooms['т.п.'] = NounCaseFormKeeper(word, *args, path=path + ('Творительный падеж', ))
        self.rooms['п.п.'] = NounCaseFormKeeper(word, *args, path=path + ('Предложный падеж', ))


class NounCaseFormKeeper(FormKeeper):
    def __init__(self, word: str, *args, path=()):
        super().__init__()

        self.default_key = 'ед.ч.' if 'мн.ч.' not in args else 'мн.ч.'

        if 'ед.ч.' in args:
            self.rooms['ед.ч.'] = '+' if 'Именительный падеж' in path else self.ask(word, path)
        elif 'мн.ч.' in args:
            self.rooms['мн.ч.'] = '+' if 'Именительный падеж' in path else self.ask(word, path)
        else:
            self.rooms['ед.ч.'] = '+' if 'Именительный падеж' in path else self.ask(word, path + ('единственное число', ))
            self.rooms['мн.ч.'] = self.ask(word, path + ('множественное число', ))


class AdjSingularFormKeeper(FormKeeper):
    def __init__(self, word: str, *args, path=()):
        super().__init__()

        self.default_key = 'м.р.'
        mascul_neu_preset = {
            'р.п.': self.ask(word, path=path + ('мужской/средний род', 'родительный падеж')),
            'д.п.': self.ask(word, path=path + ('мужской/средний род', 'дательный падеж')),
            'т.п.': self.ask(word, path=path + ('мужской/средний род', 'творительный падеж')),
            'п.п.': self.ask(word, path=path + ('мужской/средний род', 'предложный падеж'))
        }

        mascul_preset = mascul_neu_preset
        mascul_preset['и.п.'] = '+'
        mascul_preset['в.п.'] = mascul_neu_preset['р.п.']

        neu_preset = mascul_neu_preset
        neu_preset['и.п.'] = self.ask(word, path=path + ('средний род', 'именительный/винительный падеж'))
        neu_preset['в.п.'] = neu_preset['и.п.']

        fem_case = self.ask(word, path=path + ('женский род', 'родительный/дательный/творительный/предложный падеж'))

        self.rooms['м.р.'] = AdjCaseFormKeeper(word, *args, path=path + ('мужской род', ), preset=mascul_preset)
        self.rooms['с.р.'] = AdjCaseFormKeeper(word, *args, path=path + ('средний род', ), preset=neu_preset)
        self.rooms['ж.р.'] = AdjCaseFormKeeper(word, *args, path=path + ('женский род', ), preset={
            'р.п.': fem_case,
            'д.п.': fem_case,
            'т.п.': fem_case,
            'п.п.': fem_case
        })


class AdjCaseFormKeeper(FormKeeper):
    def __init__(self, word: str, *args, path=(), preset={}):
        super().__init__()

        self.default_key = 'и.п.'

        for caseform in (('и.п.', 'именительный падеж'),
                         ('р.п.', 'родительный падеж'),
                         ('д.п.', 'дательный падеж'),
                         ('в.п.', 'винительный падеж'),
                         ('т.п.', 'творительный падеж'),
                         ('п.п.', 'предложный падеж')):
            self.rooms[caseform[0]] = self.ask(word, path=path + (caseform[1], )) if caseform[0] not in preset else preset[caseform[0]]
