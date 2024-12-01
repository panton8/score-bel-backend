from team.models import Poll, Match, Voice
from user.models import UserProfile
from typing import Optional, Dict


class PollService:
    def __init__(self, profile: UserProfile, match: Match):
        self.profile = profile
        self.match = match
        self.poll = self.__get_poll_by_match(match)

    def __get_poll_by_match(self, match: Match) -> Poll:
        poll, _ = Poll.objects.get_or_create(match=match)
        return poll

    def is_profile_voted(self) -> Optional[Dict]:
        profile_voice = Voice.objects.filter(profile=self.profile, poll=self.poll)
        if not profile_voice.exists():
            return None

        voice = profile_voice.first().choice

        return voice

    def get_poll_result(self) -> Dict:
        all_voices = Voice.objects.filter(poll=self.poll)
        all_voices_count = all_voices.count()
        home_win = all_voices.filter(choice=Voice.ChoiceType.HOME_WIN).count() / all_voices_count * 100
        away_win = all_voices.filter(choice=Voice.ChoiceType.AWAY_WIN).count() / all_voices_count * 100
        draw = all_voices.filter(choice=Voice.ChoiceType.DRAW).count() / all_voices_count * 100

        return {'home_win': home_win, 'away_win': away_win, 'draw': draw}

    def make_voice(self,  voice_value: str):
        Voice.objects.create(profile=self.profile, poll=self.poll, choice=voice_value)
