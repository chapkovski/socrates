from django.apps import AppConfig
from django.conf import settings


class FirstConfig(AppConfig):
    name = 'first'
    verbose_name = "First"

    def ready(self):
        t = settings.TEMPLATES[0]
        t['OPTIONS']['builtins'] = [
            'otree.templatetags.otree',
            'django.templatetags.i18n'
        ]


