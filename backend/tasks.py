from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import func
from config import db, app
from models import Reservation

# this job looks for reservations that have expired and updates their status field to 'expired', checks every minute
def update_expired_status():
    with app.app_context():
        expired_reservations = Reservation.query.filter(Reservation.expires_at <= func.now(), Reservation.status != 'expired').all()

        for reservation in expired_reservations:
            reservation.status = 'expired'

        db.session.commit()

scheduler = BackgroundScheduler()
scheduler.add_job(func=update_expired_status, trigger="interval", minutes=1)
scheduler.start()