from sqlalchemy import create_engine
from sqlalchemy.orm import (scoped_session, sessionmaker)
from sqlalchemy.pool import NullPool


def create_psql_engine(postgres_url, pool_size, max_over_flow, pool_recycle,
                       null_pool=False,
                       pool_use_lifo=False):
    engine_kwarg = dict()
    if null_pool:
        engine_kwarg['poolclass'] = NullPool
    else:
        engine_kwarg['pool_size'] = pool_size
        engine_kwarg['max_overflow'] = max_over_flow
        engine_kwarg['pool_recycle'] = pool_recycle
        engine_kwarg['pool_use_lifo'] = pool_use_lifo

    return create_engine(postgres_url, echo=False, **engine_kwarg)


def create_psql_session(engine):
    session_factory = sessionmaker(bind=engine)
    session_cls = scoped_session(session_factory)
    session = session_cls()
    return session
