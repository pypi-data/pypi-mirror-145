"""A Russian text generator based on templating texts and word picking"""

__version__ = "0.4.1"

from WordDict.WordList import WordList
import os.path


def user_interact(db):
    print('Введите слова:')
    while True:
        print()
        word = input()
        if len(word) == 0:
            break
        tokens = word.split(sep=' ')
        name = tokens[0]
        tags = tokens[1:] if len(tokens) > 1 else ()
        db.insert(name, tags)

    print('Введите теги:')
    while True:
        print()
        tags = input()
        if len(tags) == 0:
            break
        print(db.get(*tags.split()))


def main():
    db = WordList()

    forms_db = "forms.yaml"
    tags_db = "tags.yaml"

    if os.path.isfile(forms_db) and os.path.isfile(tags_db):
        with open(forms_db, mode='r', encoding='utf-8') as formsin:
            with open(tags_db, mode='r', encoding='utf-8') as tagsin:
                db.read(formsin=formsin, tagsin=tagsin)

    try:
        user_interact(db)
    finally:
        with open(forms_db, mode='a', encoding='utf-8') as formsout:
            with open(tags_db, mode='a', encoding='utf-8') as tagsout:
                db.flush(formsout=formsout, tagsout=tagsout)


if __name__ == '__main__':
    main()
