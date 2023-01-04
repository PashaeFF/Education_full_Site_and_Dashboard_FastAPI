from fastapi import Depends
from sqlalchemy.orm import Session
from datetime import datetime
import models, database

def time_calculate(seconds):
    if seconds < 10:
        return "indi"
    if 10 < seconds < 60:
        return str(seconds).split(".")[0] + " saniyə əvvəl"
    if 60 < seconds < 120:
        return "1 dəqiqə əvvəl"
    if 120 < seconds < 3600:
        return str( seconds / 60 ).split(".")[0] + " dəqiqə əvvəl"
    if 3600 < seconds < 7200:
        return "1 saat qabaq"
    if 7200 < seconds < 86400:
        return str( seconds / 3600 ).split(".")[0] + " saat əvvəl"
    if 86400 < seconds < 172800:
        return "1 gün əvvəl"
    if 172800 < seconds < 604800:
        return str( seconds / 86400 ).split(".")[0] + " gün əvvəl"
    if 604800 < seconds < 1209600:
        return "1 həftə əvvəl"
    if 1209600 < seconds < 4838400:
        return str( seconds / 1209600 ).split(".")[0] + " həftə əvvəl"
    if 4838400 < seconds < 9676800:
        return "1 ay qabaq"
    if 9676800 < seconds < 116121600:
        return str( seconds / 604800 ).split(".")[0] + " həftə əvvəl"
    if 116121600 < seconds < 232243200:
        return "1 il əvvəl"
    if 232243200 < seconds:
        return "İllər əvvəl"

def messages_time(db: Session = database.get_db()):
    all_messages = db.query(models.AdminMessages).all()
    messages_time = []
    for i in all_messages:
        message_time = datetime.now() - i.created_at_date
        seconds = message_time.total_seconds()
        messages_time.append({"message_id": i.id, "m_time":time_calculate(seconds)})
    return messages_time