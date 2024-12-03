import factory
from django.test import TestCase

from team.models import Voice
from team.services.poll_service import PollService
from team.testing.factories import MatchFactory, PollFactory, VoiceFactory
from user.testing.factories import UserProfileFactory


class TestPollService(TestCase):
    def setUp(self):
        self.profile = UserProfileFactory()
        self.match = MatchFactory()
        self.service = PollService()

    def test_poll_service__profile_voice__without_voice(self):
        res = self.service.is_profile_voted(self.profile, self.match)
        self.assertIsNone(res)

    def test_poll_service__profile_voice__with_voice(self):
        poll = PollFactory(match=self.match)
        VoiceFactory(profile=self.profile, choice=Voice.ChoiceType.DRAW, poll=poll)
        res = self.service.is_profile_voted(self.profile, self.match)
        self.assertEqual(res, 'draw')

    def test_poll_service__make_voice__ok(self):
        voice_before = Voice.objects.filter(profile=self.profile).count()
        self.service.make_voice(self.profile, self.match, Voice.ChoiceType.AWAY_WIN)
        voice_after = Voice.objects.filter(profile=self.profile).count()

        self.assertEqual(voice_before, 0)
        self.assertEqual(voice_after, 1)

    def test_poll_service__get_poll_results__no_voice(self):
        _v = Voice.ChoiceType
        poll = PollFactory(match=self.match)
        VoiceFactory.create_batch(
            5,
            poll=poll,
            choice=factory.Iterator([_v.HOME_WIN, _v.DRAW, _v.DRAW, _v.AWAY_WIN, _v.DRAW]))

        res = self.service.get_poll_result(self.match)

        self.assertDictEqual(res, {'home_win': 20, 'away_win': 20, 'draw': 60,
                                   'home_win_count': 1, 'away_win_count': 1, 'draw_count': 3})

    def test_poll_service__get_poll_results_withount_voices__ok(self):
        PollFactory(match=self.match)
        res = self.service.get_poll_result(self.match)

        self.assertDictEqual(res, {'home_win': 0, 'away_win': 0, 'draw': 0,
                                   'home_win_count': 0, 'away_win_count': 0, 'draw_count': 0})