from team.models import Discussion, DiscussionMessage


class DiscussionService:
    def get_discussion(self, match):
        discussion, _ = Discussion.objects.get_or_create(match=match)
        return discussion

    def get_discussions_messages(self, discussion):
        messages = DiscussionMessage.objects.filter(discussion=discussion).order_by('-created_at')
        return messages

    def add_message_to_discussion(self, profile, discussion, message):
        DiscussionMessage.objects.create(discussion=discussion, message=message, profile=profile)
