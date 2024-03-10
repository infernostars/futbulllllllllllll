from typing import TypeVar

T = TypeVar("T")


def an(text):
    if text[0].lower() in "a, e, i, o, u":
        return f'an {text}'
    else:
        return f'a {text}'


def list_english(lst):
    if not lst:
        return ''
    elif len(lst) == 1:
        return str(lst[0])
    elif len(lst) == 2:
        return f"{str(lst[0])} and {str(lst[1])}"
    else:
        return ', '.join(str(item) for item in lst[:-1]) + ', and ' + str(lst[-1])
