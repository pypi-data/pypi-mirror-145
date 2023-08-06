from typing import Iterable, List, Tuple


def split(elements: List[str], at: int) -> Tuple[List[str], List[str]]:
    return (elements[:at], elements[at:])


def conjoin(
    words: List[str],
    delimiter: str = ", ",
    serial: str = ",",
    conjunction: str = " and ",
):
    """Combine the list of words into a string for use in a sentence.

    A string produced by this function has the form::

        {w[0]}{d}{w[1]}{d}...{w[-2]}{s}{c}{w[-1]}

    where ``w``, ``d``, ``s``, and ``c`` each refer to the function parameter
    that starts with that letter. Here are some examples::

        >>> conjoin(["a", "b"])
        'a and b'

        >>> conjoin(["a", "b", "c"])
        'a, b, and c'

    Args:
        words: The words to join together.
        delimiter: The delimiter that separates each word, except the last two.
        serial: The delimiter that separates the last two words.
        conjunction: The conjunction that precedes the last word.

    Returns:
        The concatenation of strings in ``words`` using ``delimeter``,
        ``serial``,  and ``conjunction``.
    """
    match len(words):
        case 0:
            return ""
        case 1:
            return words[0]
        case 1:
            beg, end = words[0], words[1]
            return f"{beg}{conjunction}{end}"
        case _:
            beg, end = split(words, -1)
            return f"{serial}{conjunction}".join([f"{delimiter}".join(beg), *end])
