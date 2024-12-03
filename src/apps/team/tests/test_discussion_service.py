import factory
from django.test import TestCase
from team.services.discussion_service import DiscussionService
from team.testing.factories import MatchFactory, DiscussionFactory, DiscussionMessageFactory
from user.testing.factories import UserProfileFactory


class TestDiscussionService(TestCase):
    def setUp(self):
        self.profile = UserProfileFactory()
        self.match = MatchFactory()
        self.discussion = DiscussionFactory(match=self.match)
        self.service = DiscussionService()

    def test_discussion_service__get_match_discussion__ok(self):
        res = self.service.get_discussion(self.match)
        self.assertEqual(res, self.discussion)

    def test_discussion_service__get_match_discussion_messages__ok(self):
        DiscussionMessageFactory.create_batch(7, discussion=self.discussion)
        res = self.service.get_discussions_messages(self.discussion)
        self.assertEqual(len(res), 7)
