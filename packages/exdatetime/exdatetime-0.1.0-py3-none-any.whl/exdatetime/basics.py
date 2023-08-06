class date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
class check:
    def istype(x, t, s):
        if type(x) != t:
            raise ValueError(f"Type of {s} is non-{t}: {type(x)}")
    def inrange(x, l, r, s):
        if not l <= x <= r:
            raise ValueError(f"{s} violates [{l}, {r}]")
    def inlbound(x, l, s):
        if x < l:
            raise ValueError(f"{s} should not be less than {l}")
    def inrbound(x, r, s):
        if x > r:
            raise ValueError(f"{s} should not be greater than {r}")
    def isnonzero(x, s):
        if x == 0:
            raise ValueError(f"{s} should be non-zero")