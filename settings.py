from os import environ
import os

EXTENSION_APPS = ['second', 'first', 'cloudcapturer']

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOME_DEFAULTS = dict(
    sec_waiting_too_long=150,
    seconds_allow_exit=60,
    msg_till_allowed_exit='Please chat for at least',
    seconds_forced_exit=1800,
    msg_forced_exit='Your chat about the best answer will end automatically in',
    time_to_start='YYYY-MM-DD 00:00 EST',
    time_bonus=0.0,
    time_to_proceed=0,
    fee_for_correct=0.5,
    study_length_min=10,
    for_prolific=False,
    prolific_redirect_url='http://www.WEBSITE.com',
    blocking=True,
    blocking_attempts=3,
)
standard_app_seq = [
    'starter',
    'first',
    'second',
    'questionnaire',
    'last'
]
SESSION_CONFIGS = [
    dict(
        name='bare',
        display_name="bare prolific q only",
        num_demo_participants=1,
        app_sequence=[
            'starter',
            'prol'
        ],
        vignette='asdf',

        **SOME_DEFAULTS
    ),
    dict(
        name='first',
        display_name="first",
        num_demo_participants=1,
        app_sequence=[
            'starter',
            'first'
        ],
        vignette='asdf',
        **SOME_DEFAULTS
    ),
    dict(
        name='second',
        display_name="chat_only",
        num_demo_participants=2,
        app_sequence=['starter', 'second'],
        vignette='asdf',
        **SOME_DEFAULTS,
        param_name='dependent'
    ),
    dict(
        name='solo_reasoning',
        display_name="Solo reasoning - essay",
        num_demo_participants=2,
        app_sequence=standard_app_seq,
        vignette='asdf',
        param_name='solo_reasoning',
        chat=False,
        **SOME_DEFAULTS
    ),
    dict(
        name='no_reward',
        display_name="No reward - essay",
        num_demo_participants=2,
        app_sequence=standard_app_seq,
        vignette='asdf',
        param_name='no_reward',
        chat=False,
        **SOME_DEFAULTS
    ),
    dict(
        name='dependent',
        display_name="Dependent reward - chat",
        num_demo_participants=2,
        app_sequence=standard_app_seq,
        vignette='asdf',
        param_name='dependent',
        chat=True,

        **SOME_DEFAULTS
    ),
    dict(
        name='independent',
        display_name="Independent reward - chat",
        num_demo_participants=2,
        app_sequence=standard_app_seq,
        vignette='asdf',
        param_name='independent',
        chat=True,
        **SOME_DEFAULTS
    ),

]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc="",

)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ROOMS = [dict(name='prolific', display_name='For Prolific users')]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '017x2njo5bj4r7)4gd9(wrg(b%v$@@9*0hsss3_&0r*ku(t9bs'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
APPEND_SLASH = True

COUNTRIES_FIRST = ['US', 'GB']
COUNTRIES_FIRST_BREAK = '-------'
COUNTRIES_FIRST_REPEAT = True

INSTALLED_APPS = [
    'otree',
    'webpack_loader',
    'rest_framework',
    'rest_framework.authtoken',
    'django_countries',
    'cloudcapturer',
    'django.contrib.humanize'
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
