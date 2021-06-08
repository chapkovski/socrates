from django.apps import AppConfig
from django.conf import settings
from django.db.utils import OperationalError
from django.db.models.signals import post_migrate, class_prepared, pre_migrate
from django.db.backends.signals import connection_created


class ProlConfig(AppConfig):
    name = 'prol'
    verbose_name = "prol"

    def ready(self):
        t = settings.TEMPLATES[0]
        t['OPTIONS']['builtins'] = [
            'otree.templatetags.otree',
            'django.templatetags.i18n'
        ]


