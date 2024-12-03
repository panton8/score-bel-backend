from team.models import Poll, Match, Voice
from user.models import UserProfile
from typing import Optional, Dict


class PollService:

    def __get_poll_by_match(self, match: Match) -> Poll:
        poll, _ = Poll.objects.get_or_create(match=match)
        return poll

    def is_profile_voted(self, profile: UserProfile, match: Match) -> Optional[Dict]:
        poll = self.__get_poll_by_match(match)
        profile_voice = Voice.objects.filter(profile=profile, poll=poll)
        if not profile_voice.exists():
            return None

        voice = profile_voice.first().choice

        return voice

    def get_poll_result(self, match: Match) -> Dict:
        poll = self.__get_poll_by_match(match)
        all_voices = Voice.objects.filter(poll=poll)
        all_voices_count = all_voices.count()

        if not all_voices_count:
            return {'draw_count': 0, 'away_win_count': 0, 'home_win_count': 0,
                'home_win': 0, 'away_win': 0, 'draw': 0}

        home_win_count = all_voices.filter(choice=Voice.ChoiceType.HOME_WIN).count()
        away_win_count = all_voices.filter(choice=Voice.ChoiceType.AWAY_WIN).count()
        draw_count = all_voices.filter(choice=Voice.ChoiceType.DRAW).count()
        home_win = home_win_count / all_voices_count * 100
        away_win = away_win_count / all_voices_count * 100
        draw = draw_count / all_voices_count * 100

        return {'draw_count': draw_count, 'away_win_count': away_win_count, 'home_win_count': home_win_count,
                'home_win': home_win, 'away_win': away_win, 'draw': draw}

    def make_voice(self, profile: UserProfile, match: Match, voice_value: str):
        poll = self.__get_poll_by_match(match)
        Voice.objects.create(profile=profile, poll=poll, choice=voice_value)