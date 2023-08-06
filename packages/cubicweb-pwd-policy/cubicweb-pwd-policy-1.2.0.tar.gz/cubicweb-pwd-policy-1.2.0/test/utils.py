from cubicweb.devtools import (
    DEFAULT_SOURCES,
    DEFAULT_PSQL_SOURCES,
)

DEFAULT_SOURCES['admin']['password'] = \
    DEFAULT_PSQL_SOURCES['admin']['password'] = \
    'pas650RDw$rd'


class PSWCubicConfigMixIn(object):

    @classmethod  # XXX could be turned into a regular method
    def init_config(cls, config):
        config.default_admin_config['password'] = DEFAULT_SOURCES[
            'admin']['password']
        super(PSWCubicConfigMixIn, cls).init_config(config)
