import pandas as pd

from .constants import ALL_ACTIVE
from .mixins import JsonMixin, SlugMixin

class Achievement(JsonMixin, SlugMixin):
    DATE_FORMAT = '%b %Y'

    def __init__(
        self,
        name,
        name_sub=None,
        location=None,
        description=None,
        bullet=None,
        link=None,
        active=None
    ):
        self.name = name
        self.name_sub = name_sub
        self.location = location
        self.description = description
        self.bullet = bullet or []
        self.link = link
        self.active = active or ALL_ACTIVE

        super().__init__()


class AchievementTime(Achievement):
    def __init__(
        self,
        name,
        name_sub=None,
        time=None,
        location=None,
        description=None,
        bullet=None,
        link=None,
        active=None
    ):
        super().__init__(name, name_sub, location, description, bullet, link, active)
        self.time = time

        if isinstance(self.time, str):
            self.time = pd.Period(self.time, 'M')

    def _serialize(self):
        obj = {}
        if self.time:
            obj['time'] = self.time
            self.time = self.time.strftime(Achievement.DATE_FORMAT)

        return obj

    def __lt__(self, other):
        return self.time < other.time
    def __gt__(self, other):
        return self.time > other.time

class AchievementDuration(Achievement):
    def __init__(
        self,
        name,
        name_sub=None,
        time_start=None,
        time_end=None,
        location=None,
        description=None,
        bullet=None,
        link=None,
        active=None
    ):
        super().__init__(name, name_sub, location, description, bullet, link, active)
        self.time_start = time_start
        self.time_end = time_end

        if isinstance(self.time_start, str):
            self.time_start = pd.Period(self.time_start, 'M')
        if isinstance(self.time_end, str):
            self.time_end = pd.Period(self.time_end, 'M')

    def _serialize(self):
        obj = {}
        if self.time_start:
            obj['time_start'] = self.time_start
            self.time_start = self.time_start.strftime(Achievement.DATE_FORMAT)

        obj['time_end'] = self.time_end
        if self.time_end:
            self.time_end = self.time_end.strftime(Achievement.DATE_FORMAT)
        else:
            self.time_end = 'Present'

        return obj

    def __lt__(self, other):
        if self.time_end == other.time_end:
            return self.time_start > other.time_start
        elif None not in [self.time_end, other.time_end]:
            return self.time_end < other.time_end
        elif self.time_end is None:
            return False
        elif other.time_end is None:
            return True
        raise Exception('failed __lt__ comparison')
    def __gt__(self, other):
        if self.time_end == other.time_end:
            return self.time_start < other.time_start
        elif None not in [self.time_end, other.time_end]:
            return self.time_end > other.time_end
        elif self.time_end is None:
            return True
        elif other.time_end is None:
            return False
        raise Exception('failed __gt__ comparison')
