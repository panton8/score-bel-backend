import logging

from django.core.management.base import BaseCommand as DjangoBaseCommand


class BaseCommand(DjangoBaseCommand):
    prefix = '[Command]'
    help = 'Command help.'
    logger = logging.getLogger('django')

    def __init__(self):
        super().__init__()
        self.total = 0
        self.processed = 0
        self.errors = 0
        self.skipped = 0

    def log(self, msg: str):
        self.logger.info(f'{self.prefix} {msg}')

    def log_exc(self, msg: str, extra=None):
        self.logger.exception(f'{self.prefix} {msg}', extra=extra)

    def _log_result(self):
        self.log(f'Migration finished. total/processed/skipped/errors: {self.total}/{self.processed}/{self.skipped}/{self.errors}')
