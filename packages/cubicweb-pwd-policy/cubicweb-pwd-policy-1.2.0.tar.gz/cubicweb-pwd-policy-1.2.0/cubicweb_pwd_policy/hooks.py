# -*- coding: utf-8 -*-
# copyright 2018-2022 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""cubicweb-pwd-policy specific hooks and operations"""

from cubicweb import ValidationError

from cubicweb.predicates import is_instance
from cubicweb.server.hook import Hook

from cubicweb_pwd_policy import accept_password


class EnsurePassowrdCompliancyHook(Hook):
    """password must be complient to ANSI security recommendations
    except anon password (cw developpement facility)
    """
    __regid__ = 'pwd.compliancy'
    __select__ = (Hook.__select__ & is_instance('CWUser'))
    events = ('before_add_entity', 'before_update_entity')

    def __call__(self):
        if self.entity.login != 'anon':
            upassword = self.entity.cw_edited.get('upassword', None)
            if upassword and not accept_password(upassword, self._cw.encoding):
                msg = self._cw._('non-compliant-to-pwd_policy')
                raise ValidationError(
                    self.entity.eid, {'upassword-subject': msg})
