from datetime import timedelta

from django_filters import rest_framework as filters, DateFilter

from core.utils.dateutils import gmt3_date_to_utc_dtm
from team.models import Match


class MatchFilter(filters.FilterSet):
    date = filters.DateFilter(method='filter_date')

    class Meta:
        model = Match
        fields = ('date', 'tournament', 'full_time')

    def filter_date(self, qs, name, value):
        if not value:
            return qs

        start_time = gmt3_date_to_utc_dtm(value)
        end_time = gmt3_date_to_utc_dtm(value+timedelta(days=1))

        qs = qs.filter(start_time__gte=start_time, start_time__lte=end_time)

        return qs
