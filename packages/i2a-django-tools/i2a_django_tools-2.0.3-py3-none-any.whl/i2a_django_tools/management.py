from abc import ABC

from django.core.management import BaseCommand, CommandError
from django.db import transaction

from i2a_django_tools.database import soft_atomic


class DryRunByDefaultBaseCommand(BaseCommand, ABC):
    """
        Put operation in transaction block,
        operation will be saved only with execute flag.
    """
    def add_arguments(self, parser):
        parser.add_argument('--execute', dest='execute', action='store_true')
        parser.add_argument('--soft-atomic', dest='use_soft_atomic', action='store_true')

    def execute(self, *args, **options):
        assert 'execute' in options, 'execute must be in options'
        execute = options['execute']
        use_soft_atomic = options['use_soft_atomic']
        if not execute and use_soft_atomic:
            raise CommandError(
                "Soft atomic can be used only with execute flag."
            )
        if execute:
            self.stdout.write("Script running execute mode.")
        else:
            self.stdout.write("Script running in dry-run mode, to save changes, add --execute.")

        atomic = self.get_atomic(use_soft_atomic)
        with atomic():
            super().execute(*args, **options)
            if not execute:
                self.stdout.write(
                    f"Rolling back all changes..."
                )
                transaction.set_rollback(True)
        self.stdout.write(
            f"Script ended"
        )

    @staticmethod
    def get_atomic(use_soft_atomic: bool):
        if use_soft_atomic:
            return soft_atomic
        return transaction.atomic


class CustomBackgroundTaskBaseCommand(BaseCommand, ABC):

    def add_arguments(self, parser):
        parser.add_argument('--soft-atomic', dest='use_soft_atomic', action='store_true')
        parser.add_argument('--not-atomic', dest='not_use_atomic', action='store_true')

    def execute(self, *args, **options):
        use_soft_atomic = options['use_soft_atomic']
        not_use_atomic = options['not_use_atomic']
        if use_soft_atomic and not_use_atomic:
            raise CommandError('Can use no-atomic and soft-atomic together')

        if not_use_atomic:
            self.stdout.write("Script running without atomic.")
        elif use_soft_atomic:
            self.stdout.write("Script running with soft_atomic.")
        else:
            self.stdout.write("Script running with atomic.")

        if not_use_atomic:
            self.execute_and_wrap_exception(*args, **options)
        else:
            atomic = self.get_atomic(use_soft_atomic)
            with atomic():
                self.execute_and_wrap_exception(*args, **options)
        self.stdout.write(f"Script ended")

    def execute_and_wrap_exception(self, *args, **options):
        try:
            super().execute(*args, **options)
        except Exception:
            raise

    @staticmethod
    def get_atomic(use_soft_atomic: bool):
        if use_soft_atomic:
            return soft_atomic
        return transaction.atomic
