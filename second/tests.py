from otree.api import Currency as c, currency_range, Submission, SubmissionMustFail
from .pages import *
from ._builtin import Bot
import random


def answer_strategy(group):
    """

    if they hold opposite positions:
        there is X1% the wrong one will change to correct, and correct holder will keep it
        there is X2% the correct holder will change to incorrect and the wrong one will keep it
        X3% chance that they each will keep their original positions
        X4% they inverse (the wrong holder will switch )
    these values are different for independent and dependent treatments
    for no_reward and solo treatments there is a certain probability (<50%) to change the position. this parameter is
    different for no_reward and solo.

    """
    ego, alter = group.get_players()
    ego_pos = ego.participant.vars.get('position')
    alter_pos = alter.participant.vars.get('position')
    assert ego_pos != alter_pos, 'SOMETHING IS WRONG WITH MATCHING'
    dep_weight_probs = (0.6, 0.15, 0.15, 0.10)
    indep_weight_probs = (0.4, 0.15, 0.35, 0.10)
    if ego.treatment == 'dependent':
        weight_probs = dep_weight_probs
    else:
        weight_probs = indep_weight_probs

    correct = ego.subsession.correct
    same_pos_for_both = {ego.id_in_group: ego_pos, alter.id_in_group: alter_pos}

    case = random.choices([1, 2, 3, 4], weights=weight_probs, k=1)[0]
    if case == 1:
        #  the wrong one will change to correct, and correct holder will keep it
        resp = {ego.id_in_group: correct, alter.id_in_group: correct}
    elif case == 2:
        # the correct holder will change to incorrect and the wrong one will keep it
        resp = {ego.id_in_group: not correct, alter.id_in_group: not correct}
    elif case == 3:
        # they each will keep their original positions
        resp = same_pos_for_both
    else:
        # they inverse (the wrong holder will switch )
        resp = {ego.id_in_group: alter_pos, alter.id_in_group: ego_pos}
    return resp


group_strategies = {}


class PlayerBot(Bot):
    def play_round(self):
        yield Instructions
        for i in range(random.randint(0, 2)):
            yield SubmissionMustFail(ComprehensionCheck, {'cq_3': True, 'cq_6': True, 'cq_4': False})
        yield ComprehensionCheck, {'cq_3': True, 'cq_6': True, 'cq_4': True}
        ans = dict(
            confidence=random.randint(0, 10),
            answer=random.choice([True, False])
        )
        if self.player.in_chat_treatment:

            yield Submission(DiscussionPage, check_html=False)
            if not group_strategies.get(self.group.pk):
                group_strategies[self.group.pk] = answer_strategy(self.group)
            ans['answer'] = bool(group_strategies[self.group.pk][self.player.id_in_group])
        else:
            yield Submission(EssayPage, {'essay': 'bot essay'}, check_html=False)
            r = random.random()
            if self.player.treatment == 'no_reward':
                threshold = 0.85
            else:
                threshold = 0.70
            if r > threshold:
                ans['answer'] = not self.participant.vars.get('position')
            else:
                ans['answer'] = self.participant.vars.get('position')

        yield Submission(SecondOpinion, ans, check_html=False)
