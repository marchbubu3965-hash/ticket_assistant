from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from scheduler.jobs import run_ticket_job


class SchedulerService:
    """
    單次排程服務
    """

    def __init__(self):
        self.scheduler = BackgroundScheduler(timezone="Asia/Taipei")
        self.scheduler.start()

    def schedule_once(
        self,
        *,
        run_at: datetime,
        job_id: str,
        job_kwargs: dict,
    ):
        """
        單次排程
        """
        self.scheduler.add_job(
            func=run_ticket_job,
            trigger="date",
            run_date=run_at,
            kwargs=job_kwargs,
            id=job_id,
            replace_existing=True,
        )

    def shutdown(self):
        self.scheduler.shutdown()
