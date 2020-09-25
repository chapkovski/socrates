from os import environ
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SESSION_CONFIGS = [
    dict(
        name='first',
        display_name="first",
        num_demo_participants=1,
        app_sequence=['first'],
        vignette='asdf'
    ),
    dict(
        name='second',
        display_name="second",
        num_demo_participants=2,
        app_sequence=['second'],
        vignette='asdf'
    ),
    dict(
        name='together',
        display_name="Full game",
        num_demo_participants=2,
        app_sequence=['first', 'second'],
        vignette='asdf'
    ),
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = []

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '017x2njo5bj4r7)4gd9(wrg(b%v$@@9*0hsss3_&0r*ku(t9bs'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
APPEND_SLASH = True
EXTENSION_APPS = ['second', 'first']
INSTALLED_APPS = [
    'otree',
    'webpack_loader',
    'rest_framework',
    'rest_framework.authtoken'
]

WEBPACK_LOADER = {
    'DEFAULT': {
        # 'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'vue/',  # must end with slash
        'STATS_FILE': os.path.join(BASE_DIR, 'gettierfront', 'webpack-stats.json'),
        'POLL_INTERVAL': 0.3,
        'TIMEOUT': None,
        'IGNORE': [r'.+\.hot-update.js', r'.+\.map']
    }
}
