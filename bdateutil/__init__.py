#  bdateutil
#  -----------
#  Adds business day logic and improved data type flexibility to
#  python-dateutil. 100% backwards compatible with python-dateutil,
#  simply replace dateutil imports with bdateutil.
#
#  Author:  ryanss <ryanssdev@icloud.com>
#  Website: https://github.com/ryanss/bdateutil
#  License: MIT (see LICENSE file)

__version__ = '0.2-dev'


import calendar
from datetime import date as basedate
from datetime import datetime as basedatetime
from datetime import time as basetime

from bdateutil.parser import parse
from bdateutil.relativedelta import relativedelta
from bdateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
from bdateutil.rrule import *


def isbday(dt, holidays=None, weekdays_off=None):
    if holidays is None:
        holidays = getattr(isbday, 'holidays', ())
    if weekdays_off is None:
        weekdays_off = getattr(isbday, 'weekdays_off', (5, 6))
    dt = parse(dt)
    return not (dt.weekday() in weekdays_off or dt in holidays)


class date(basedate):

    def __new__(self, *args, **kwargs):
        if len(args) == 1:
            args = parse(args[0]).timetuple()[:3]
        if len(args) > 2:
            if args[2] == 99:
                args = list(args)
                args[2] = calendar.monthrange(args[0], args[1])[1]
        return basedate.__new__(self, *args, **kwargs)

    @staticmethod
    def today(**kwargs):
        return basedate.today() + relativedelta(**kwargs)

    @property
    def eomday(self):
        return date(self.year, self.month,
                    calendar.monthrange(self.year, self.month)[1])


class datetime(basedatetime):

    def __new__(self, *args, **kwargs):
        if len(args) == 1:
            args = parse(args[0]).timetuple()[:6]
        if len(args) > 2:
            if args[2] == 99:
                args = list(args)
                args[2] = calendar.monthrange(args[0], args[1])[1]
        return basedatetime.__new__(self, *args, **kwargs)

    @staticmethod
    def now(**kwargs):
        return basedatetime.now() + relativedelta(**kwargs)

    @property
    def eomday(self):
        return datetime(self.year, self.month,
                        calendar.monthrange(self.year, self.month)[1],
                        self.hour, self.minute, self.second,
                        self.microsecond)


class time(basetime):

    def __new__(self, *args, **kwargs):
        if len(args) == 1:
            args = parse(args[0]).timetuple()[3:6]
        return basetime.__new__(self, *args, **kwargs)

    @staticmethod
    def now(**kwargs):
        ret = basedatetime.now() + relativedelta(**kwargs)
        if ret.date() == basedatetime.now().date():
            return ret.time()
        return ret
