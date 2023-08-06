from django.db.transaction import Atomic
from django.db import Error
from django.db import DEFAULT_DB_ALIAS


class SoftAtomic(Atomic):
    """
        Context manager built on top of original atomic.
        It's purpose is to ignore exceptions other that db-integrity errors
        (e.g. when exception is "expected" and results still should be saved
        to database.
    """

    # list of exceptions which should handled as standard Atomic would do
    # (execute rollback)
    FATAL_EXCEPTIONS = (Error,)

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type and not issubclass(exc_type, self.FATAL_EXCEPTIONS):
            exc_type = None
            exc_value = None
            traceback = None
        super(SoftAtomic, self).__exit__(exc_type, exc_value, traceback)


def soft_atomic(using=None, savepoint=True, durable=False):
    """
        Copy of atomic decorator (from django.db.transaction) for SoftAtomic
    """
    if callable(using):
        return SoftAtomic(DEFAULT_DB_ALIAS, savepoint, durable)(using)
    else:
        return SoftAtomic(using, savepoint, durable)
