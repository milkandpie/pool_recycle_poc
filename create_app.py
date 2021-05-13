import os

from flask import Flask

from create_engine import (create_psql_session, create_psql_engine)
from log import log
from models import Account


class Factory:
    def __init__(self):
        self.pid = os.getpid()

        postgres_url = os.getenv('DB_URL')
        pool_size = int(os.getenv('POOL_SIZE', 0))
        max_over_flow = int(os.getenv('MAX_OVERFLOW'))
        pool_recycle = int(os.getenv('POOL_RECYCLE', 0))
        null_pool = bool(int(os.getenv('NULL_POOL', 0)))

        log.warning(f'\n________API on {self.pid}_______')
        log.info(f'DB_URL: {postgres_url}')
        log.info(f'POOL_SIZE: {pool_size}')
        log.info(f'MAX_OVERFLOW: {max_over_flow}')
        log.info(f'POOL_RECYCLE: {pool_recycle}')
        log.info(f'USING NULL POOL: {null_pool}\n')

        self.engine = create_psql_engine(postgres_url, pool_size, max_over_flow, pool_recycle, null_pool)

    def create_app(self):
        app = Flask(__name__)

        @app.route("/accounts/<account_id>")
        def hello(account_id):
            log.info(f'Create session on {self.pid}')
            session = create_psql_session(self.engine)
            account = session.query(Account).get(account_id)
            session.close()

            if not account:
                return {}
            return account.serialize()

        return app
