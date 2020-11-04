from datetime import tzinfo, timedelta


class Lviv_TZ(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=3)

    def dst(self, dt):
        return timedelta(hours=2)

    def __repr__(self):
        return f"{self.__class__.__name__}()"
