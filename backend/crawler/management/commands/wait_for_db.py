import time  # default python module to make app sleep for a few seconds in between each db check

from django.db import connections  # to test if db connection is available
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand  # the class we need to build on in order to create our custom command

# https://docs.djangoproject.com/en/2.1/howto/custom-management-commands/#module-django.core.management


class Command(BaseCommand):  # django command to pause execution till database is available

    def handle(self, *args, **options):
        self.stdout.write("Waiting for database...")  # to print out on screen during these management commands.
        db_conn = None
        while not db_conn:
            # i.e while there is no value in db_conn,try to set to db connections and if the connection
            # is not available then django raises operational error and we raise an output and app sleeps
            # for 1 second.This repeats till the db connection is available.
            try:
                db_conn = connections["default"]
            except OperationalError:
                self.stdout.write("Database unavailable,Waiting 1 second")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available!"))
