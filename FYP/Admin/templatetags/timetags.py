from django import template
import datetime
register = template.Library()

# This functions converts the unix time stamp to python datetime
@register.filter(name='timestamp')  # registering the template tag
def timestamp(timestamp):
    try:
        # assume, that timestamp is given in seconds with decimal point
        ts = float(timestamp)
    except ValueError:
        return None
    return datetime.datetime.fromtimestamp(ts)
