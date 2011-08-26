from optparse import make_option
import os
import threading

from django.core.management.base import BaseCommand, CommandError
from django.core.management.commands.runserver import BaseRunserverCommand
from django.conf import settings

from pyvascript.utils.watch import watch as pyva_watch

class Command(BaseRunserverCommand):
    option_list = BaseRunserverCommand.option_list + (
        make_option('--disable-watch', action='store_true', dest='not_watch', default=False,
            help='Do not watch for .pyva, .coffee, and .sass files'),
    )

    def inner_run(self, *args, **options):
        if not options["not_watch"]:
            self.project_root = getattr(
                settings, "PROJECT_ROOT",
                os.path.dirname(os.path.normpath(os.sys.modules[settings.SETTINGS_MODULE].__file__))
            )

            self.stdout.write("Starting pyva watch command for %r\n" % self.project_root)
            thread = threading.Thread(target=pyva_watch, args=(self.project_root,))
            thread.start()

        super(Command, self).inner_run(*args, **options)
