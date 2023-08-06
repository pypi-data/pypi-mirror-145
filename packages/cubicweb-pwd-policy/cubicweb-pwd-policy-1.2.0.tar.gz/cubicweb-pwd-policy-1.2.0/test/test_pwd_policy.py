# -*- coding: utf-8 -*-
import unittest

from cubicweb.devtools.testlib import CubicWebTC
from cubicweb_pwd_policy import accept_password

from utils import PSWCubicConfigMixIn


class BasicPasswordPolicyTests(PSWCubicConfigMixIn, CubicWebTC):

    def test_password_strength(self):
        for psw, expected in (
            (u'iuzYEr7£zerI1PE', True),
            (u'+uzYEr7£zérIE', True),
            (u'o2ieuUYEtrz4ud', False),
            (u'o2ieuUY trz4ud', True),  # space is acceptable
            (u'o2ieuUYétrz4ud', False),
            (u'o2ieuUY$trz4ud', True),
            (u'o2uUY$rzud', False),
            (u'o2uaa$rzudpo*d2', False),
            (u'O2UAA$REZ3ED*D', False),
            (u'IuzYEr7azérIE', False),
            (u'Iuz1YEr7azérIE', False),
            (u'Iuz1YEr7azér"E', True),
            (u'Iùz1YEr7az$rIE', True)

        ):
            self.assertEqual(accept_password(psw, 'utf-8'),
                             expected)
            self.assertTrue(
                accept_password(
                    psw, 'utf-8', maxlen=10, upper=False, lower=False,
                    digit=False, other=False))
        self.assertTrue(
            accept_password(
                u'IuzYEr7azérIE', 'utf-8', maxlen=10, upper=True,
                lower=True, digit=False, other=False))
        self.assertTrue(
            accept_password(
                u'IuzYEr7azérIE', 'utf-8', maxlen=10, upper=True,
                lower=True, digit=False, other=False))
        self.assertTrue(
            accept_password(
                u'IuzYEr7£azérIE', 'utf-8', maxlen=10, upper=True,
                lower=True, digit=False, other=True))


if __name__ == '__main__':
    unittest.main()
