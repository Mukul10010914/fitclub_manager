from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from subscription_updater import update

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update.sub, 'interval', minutes=10)
    scheduler.start()