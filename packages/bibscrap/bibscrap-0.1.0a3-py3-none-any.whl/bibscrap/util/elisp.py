"""Support for Emacs Lisp S-expressions.

(- 1 2 3 4)
"""

#: In Emacs Lisp, the symbol ``nil`` has three separate meanings: it is a symbol
#: with the name "nil"; it is the logical truth value ``False``; and it is the
#: empty list (i.e., the list of zero elements).
nil = []


class kwarg:
    def __init__(self, name, value):
        self.name = name
        self.value = value


def concat(*args):
    return "".join(args)


def add(*args):
    return sum(args)


def kwarg(name, value):
    return dict(name=value)


sexpr = [print, [concat, [str, [add, 1, 2, 4]], "is cool!"]]


def getargs(sexp):
    return [apply(exp) for exp in sexp if not isinstance(exp, kwarg)]


def getkwargs(sexp):
    return {arg.name: apply(arg.value) for exp in sexp if isinstance(exp, kwarg)}


def apply(sexp):
    if not isinstance(sexp, list):
        return sexp
    else:
        if len(sexp) == 0:
            return False
        else:
            func = sexp[0]
            args = getargs(sexp)
            kwargs = getkwargs(sexp)
            return func(*args, **kwargs)
