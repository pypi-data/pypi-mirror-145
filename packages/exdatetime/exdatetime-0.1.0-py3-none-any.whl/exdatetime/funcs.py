from exdatetime.basics import *
def isleap(y, isjulian = True):
    check.istype(y, int, "year")
    check.isnonzero(y, "Year")
    check.istype(isjulian, bool, "isjulian")
    if isjulian and y < 1582:
        if y < 0:
            return (-y) % 4 == 1
        return y % 4 == 0
    return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)
def daysofmonth(y, m, isjulian = True):
    check.istype(y, int, "year")
    check.isnonzero(y, "Year")
    check.istype(m, int, "month")
    check.inrange(m, 1, 12, "Month")
    check.istype(isjulian, bool, "isjulian")
    if m == 2:
        if isleap(y, isjulian):
            return 29
        return 28
    elif m == 4 or m == 6 or m == 9 or m == 11:
        return 30
    return 31
def cmpdate(d1, d2):
    check.istype(d1, date, "date1")
    check.istype(d2, date, "date2")
    if d1.year == d2.year:
        if d1.month == d2.month:
            if d1.day == d2.day:
                return 0
            elif d1.day > d2.day:
                return 1
            return -1
        elif d1.month > d2.month:
            return 1
        return -1
    elif d1.year > d2.year:
        return 1
    return -1