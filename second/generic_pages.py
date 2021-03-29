from ._builtin import Page as oTreePage
from .models import TimeTracker
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)


class Page(oTreePage):
    time_tracker_field = None

    def get(self, *args, **kwargs):
        t, _ = TimeTracker.objects.get_or_create(owner=self.participant,
                                                 page=self.__class__.__name__,
                                                 period=self.player.round_number,
                                                 app_name=self._lookup.app_name,
                                                 defaults=dict(get_time=datetime.now(timezone.utc), ))
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        try:
            t = TimeTracker.objects.get(owner=self.participant,
                                        page=self.__class__.__name__,
                                        period=self.player.round_number,
                                        app_name=self._lookup.app_name
                                        )
            t.post_time = datetime.now(timezone.utc)
            t.seconds_on_page = (t.post_time - t.get_time).seconds
            t.save()
            if self.time_tracker_field:
                setattr(self.player, self.time_tracker_field, t.seconds_on_page)
        except (TimeTracker.DoesNotExist, TimeTracker.MultipleObjectsReturned):
            logger.warning('Tracker not found')

        return super().post(*args, **kwargs)
