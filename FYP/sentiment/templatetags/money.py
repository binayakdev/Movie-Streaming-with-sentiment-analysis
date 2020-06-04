from django import template
import math
register = template.Library()

millnames = ['', ' Thousand', ' Million', ' Billion', ' Trillion']

# This function amount in digits to words
@register.filter(name='millify')
def millify(n):
    n = float(n)
    millidx = max(0, min(len(millnames)-1,
                         int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])
