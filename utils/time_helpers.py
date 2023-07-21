from datetime import datetime
from pytz import utc
def utc_now():
    return datetime.now().replace(tzinfo=utc)