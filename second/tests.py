from otree.api import Currency as c, currency_range, Submission, SubmissionMustFail
from .pages import *
from ._builtin import Bot
import random


def answer_strategy(group):
    """
    if they hold opposite positions:
        there is 60% the wrong one will change to correct, and correct holder will keep it
        there is 15% the correct holder will change to incorrect and the wrong one will keep it
        15% chance that they each will keep their original positions
        10% they inverse (the wrong holder will switch )

    if they hold the same correct position there is 85% they keep it
    if they hold the same incorrect position there is 65% they keep it

    """
    ego, alter = group.get_players()
    opposite_weight_probs = (0.6, 0.15, 0.15, 0.10)
    correct_prob = 0.85
    incorrect_prob = 0.65
    ego_pos = ego.participant.vars.get('position')
    alter_pos = alter.participant.vars.get('position')

    correct = ego.subsession.correct
    same_pos_for_both = {ego.id_in_group: ego_pos, alter.id_in_group: alter_pos}
    r = random.random()
    if ego_pos == alter_pos:

        if ego_pos == correct:
            if r < correct_prob:
                resp = same_pos_for_both
            else:
                resp = {ego.id_in_group: not ego_pos, alter.id_in_group: not alter_pos}
        else:
            if r < incorrect_prob:
                resp = same_pos_for_both
            else:
                resp = {ego.id_in_group: not ego_pos, alter.id_in_group: not alter_pos}

    else:
        case = random.choices([1, 2, 3, 4], weights=opposite_weight_probs, k=1)[0]
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
        for i in range(random.randint(0,2)):
            yield SubmissionMustFail(ComprehensionCheck, {'cq_3': True, 'cq_6': True, 'cq_4': False})
        yield ComprehensionCheck, {'cq_3': True, 'cq_6': True, 'cq_4': True}
        ans = dict(
            confidence=random.randint(0, 10),
            answer=random.choice([True, False])
        )
        if self.session.config.get('chat'):
            yield Submission(DiscussionPage, check_html=False)
            if not group_strategies.get(self.group.pk):
                group_strategies[self.group.pk] = answer_strategy(self.group)
            ans['answer'] = bool(group_strategies[self.group.pk][self.player.id_in_group])
        else:
            yield Submission(EssayPage, {'essay': 'bot essay'}, check_html=False)


        yield Submission(SecondOpinion, ans, check_html=False)
