from apscheduler.schedulers.blocking import BlockingScheduler
import pytz

sched = BlockingScheduler(timezone=pytz.timezone('Africa/Lagos'))

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=22)
def scheduled_job():
    print('This job is run every week at 10pm.')
    #your job here


sched.start()