"""cubicweb-pwd_policy application package

Password policy for cubicweb applications
"""
# -*- coding: utf-8 -*-
import unicodedata
from six import text_type as unicode


def remove_diacritics(text, encoding):
    if not isinstance(text, unicode):
        text = text.decode(encoding)
    normalized = unicodedata.normalize("NFKD", text)
    return u"".join(c for c in normalized if unicodedata.category(c) != "Mn")


def accept_password(psw, encoding, maxlen=12, upper=True, lower=True,
                    digit=True, other=True):
    """
    1. maxlen = minimum 12 characters long
    2. mandatory or optional uppercase, lowercase, numbers, special characters.
    """
    if len(psw) < maxlen:
        return False
    if not any((upper, lower, digit, other)):
        return True
    is_upper, is_lower, is_digital, is_other = False, False, False, False
    check = []
    for c in remove_diacritics(psw, encoding):
        if c.isdigit():
            is_digital = True
        elif c.isupper():
            is_upper = True
        elif c.islower():
            is_lower = True
        else:
            is_other = True
    for flag, res in ((upper, is_upper),
                      (lower, is_lower),
                      (digit, is_digital),
                      (other, is_other)):
        if flag:
            check.append(res)
    return all(check)
