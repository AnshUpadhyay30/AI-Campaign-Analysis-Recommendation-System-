# from __future__ import annotations

# import logging

# from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.triggers.cron import CronTrigger

# from src.common.config import Settings
# from src.orchestrator.pipeline import run_weekly

# LOGGER = logging.getLogger(__name__)


# def start_scheduler(settings: Settings) -> None:
#     scheduler = BlockingScheduler(timezone=settings.timezone)

#     minute, hour, _, _, day_of_week = settings.weekly_cron.split()
#     trigger = CronTrigger(minute=int(minute), hour=int(hour), day_of_week=day_of_week.lower())

#     scheduler.add_job(lambda: run_weekly(settings, rerun=False), trigger=trigger, id="weekly_run", replace_existing=True)
#     LOGGER.info("Scheduler started for cron=%s timezone=%s", settings.weekly_cron, settings.timezone)
#     scheduler.start()


from __future__ import annotations

import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from src.common.config import Settings
from src.orchestrator.pipeline import run_weekly

LOGGER = logging.getLogger(__name__)


def start_scheduler(settings: Settings) -> None:
    scheduler = BlockingScheduler(timezone=settings.timezone)

    minute, hour, day, month, day_of_week = settings.weekly_cron.split()

    trigger = CronTrigger(
        minute=minute,
        hour=hour,
        day=day,
        month=month,
        day_of_week=day_of_week
    )

    scheduler.add_job(
        lambda: run_weekly(settings, rerun=False),
        trigger=trigger,
        id="weekly_run",
        replace_existing=True
    )

    LOGGER.info("Scheduler started for cron=%s timezone=%s", settings.weekly_cron, settings.timezone)
    scheduler.start()