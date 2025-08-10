import os

def get_hour_minute_ampm_format():
    """
    Returns the strftime format string for hour:minute AM/PM without leading zero on hour, OS-agnostic.
    Windows: '%#I:%M %p', Unix: '%-I:%M %p'
    """
    if os.name == 'nt':
        return '%#I:%M %p'
    else:
        return '%-I:%M %p'
