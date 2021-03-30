from django.apps import AppConfig
from django.conf import settings


class SensConfig(AppConfig):
    name = 'cloudcapturer'
    verbose_name = "Cloud Capturer"

    def ready(self):
        t = settings.TEMPLATES[0]
        t['OPTIONS']['builtins'] = [
            'otree.templatetags.otree',
            'django.templatetags.i18n'
        ]


