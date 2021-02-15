from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

author = 'Philip Chapkovski, HSE-Moscow'

doc = """
Post-experimental questionnaire for Socrates projet
"""


class Constants(BaseConstants):
    name_in_url = 'questionnaire'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(label='In what year were you born?', min=18, max=100)
    sex = models.IntegerField(label='What is your gender?',
                              choices=[(0, 'Male'), (1, 'Female'), (2, 'Other')],
                              widget=widgets.RadioSelectHorizontal)
    race = models.IntegerField(label='Which race or races do you consider yourself to be',
                               choices=[(0, 'White'),
                                        (1, 'Black or African American'),
                                        (2, 'American Indian or Alaska Native'),
                                        (3, 'Asian'),
                                        (4, 'Native Hawaiian or Pacific Islander'),
                                        (5, 'Other')
                                        ],
                               widget=widgets.RadioSelect
                               )
    education = models.IntegerField(label='What is the highest level of education you have achieved?',
                                    choices=[(0, 'Less than high school degree'),
                                             (1,
                                              'High school graduate (high school diploma or equivalent including GED)'),
                                             (2, 'Some college but no degree'),
                                             (3, 'Associate degree in college (2-year)'),
                                             (4, 'Bachelor''s degree in college (4-year)'),
                                             (5, 'Master''s degree'),
                                             (6, 'Doctoral degree'),
                                             (7, 'Professional degree (JD, MD)')
                                             ],
                                    widget=widgets.RadioSelect
                                    )
    ses = models.IntegerField(label='What is the highest level of education your parents have achieved?',
                              choices=[(0, 'Less than high school degree'),
                                       (1, 'High school graduate (high school diploma or equivalent including GED)'),
                                       (2, 'Some college but no degree'),
                                       (3, 'Associate degree in college (2-year)'),
                                       (4, 'Bachelor''s degree in college (4-year)'),
                                       (5, 'Master''s degree'),
                                       (6, 'Doctoral degree'),
                                       (7, 'Professional degree (JD, MD)')
                                       ],
                              widget=widgets.RadioSelect
                              )
    phil_background = models.IntegerField(label='How much philosophy have you studied in college or high school?',
                                          choices=[(0, 'None (zero classes)'),
                                                   (1, 'Some (1 - 3 classes)'),
                                                   (2, 'Moderate (4 - 7 classes)'),
                                                   (3, 'A lot (More than 7 classes)'),
                                                   ],
                                          widget=widgets.RadioSelectHorizontal
                                          )
    stats_background = models.IntegerField(label='How much statistics have you studied in college or high school?',
                                           choices=[(0, 'None (zero classes)'),
                                                    (1, 'Some (1 - 3 classes)'),
                                                    (2, 'Moderate (4 - 7 classes)'),
                                                    (3, 'A lot (More than 7 classes)'),
                                                    ],
                                           widget=widgets.RadioSelectHorizontal
                                           )
    stem_background = models.BooleanField(label='Did you major in a STEM field or are you planning to do so?',
                                          choices=[(False, "No"),
                                                   (True, 'Yes')
                                                   ],
                                          widget=widgets.RadioSelectHorizontal
                                          )
    critical_background = models.BooleanField(label='Have you ever studied critical thinking?',
                                              choices=[(False, "No"),
                                                       (True, 'Yes')
                                                       ],
                                              widget=widgets.RadioSelectHorizontal
                                              )
    country_born = CountryField(verbose_name='In which country were you born?', null=True, blank=False )
    country_life = CountryField(verbose_name='In which country have you lived most of your life?', null=True, blank=False)
    survey_experience = models.IntegerField(label='Overall, how positive was your experience of this survey?',
                                            choices=[(1, 'Negative'),
                                                     (2, 'Somewhat negative'),
                                                     (3, 'Neither positive nor negative'),
                                                     (4, 'Somewhat positive'),
                                                     (5, 'Positive'),
                                                     ],
                                            widget=widgets.RadioSelectHorizontal
                                            )
    other_comments = models.LongStringField(null=True,
                                            blank=True,
                                            label='If you have any other comments that you would like to'
                                                  ' share with us, please do so here')
