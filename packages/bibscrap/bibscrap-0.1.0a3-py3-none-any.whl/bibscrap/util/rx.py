"""Support for Structured Regexp Notation (RX).

This module provides a structured ``rx`` notation for emitting regular
expression patterns that are compatible with the :py:mod:`re` module. It is
inspired by the S-expressions that are formed when using the ``rx`` and
related macros that are provided by Emacs Lisp\ [elisp_rx]_.

.. [elisp_rx] Chassell, R.J. 2009. The rx Structured Regexp Notation.
   *An Introduction to Programming in Emacs Lisp.*
   GNU Press. Boston, MA, USA. ISBN 1-882114-43-4.
   https://www.gnu.org/software/emacs/manual/html_node/elisp/Rx-Notation.html
"""

import re

"""
(rx (and "A" "B"))
"""


class rx:
    """Match the ``rx`` patterns in sequence."""

    SEP = ""
    SEXP = "{args}"

    def __init__(self, *args):
        self._args = list(args)

    def __repr__(self):
        construct = self.__class__.__name__
        args = ", ".join(map(repr, self._args))
        return f"{construct}({args})"

    def re(self):
        args = self.SEP.join(map(rx.rx_to_re, self._args))
        regexp = self.SEXP.format(args=args, self=self)
        return regexp

    @staticmethod
    def rx_to_re(arg):
        if isinstance(arg, str):
            return arg
        elif isinstance(arg, rx):
            return arg.re()
        else:
            raise TypeError


class seq(rx):
    """Match the ``rx`` patterns in sequence."""

    pass


class one(rx):
    """Match exactly one of the ``rx`` patterns."""

    SEP = "|"
    SEXP = "(?:{args})"


class unmatchable(one):
    """Refuse any match."""

    def __init__(self):
        super().__init__()

    def re(self):
        return ""


class zero_or_more(rx):
    """Match the ``rx`` patterns zero or more times."""

    SEXP = "(?:{args})*"


class opt(rx):
    """Match the ``rx`` patterns once or an empty string."""

    SEXP = "(?:{args})?"


class repeat(rx):
    """Match the ``rx`` patterns exactly ``n`` times."""

    SEXP = "(?:{args}){{{self._n}}}"

    def __init__(self, n, *args):
        self._n = n
        super().__init__(*args)


"""
(rx (seq "a" "hello"))
"""
