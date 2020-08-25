''' SrtTime class for keeping time used in SRT format. 
eg. :minutes:seconds,milliseconds, 
'''

class SrtTime(object):
    def __init__(self, string="", hours=0, mins=0, secs=0, microSecs=0, positive=True):
        if string:
            import re
            try:
                pattern = r"(-)*([0-9]+):([0-9]+):([0-9]+)[.,]([0-9]+)" #with microSecs
                m = re.match(pattern, string)
                [hours, mins, secs, microSecs] = [int(x) for x in m.groups()[1:]]
                sign = m.groups()[0]
                if sign: positive = False
            except AttributeError:
                try:
                    pattern = r"(-)*([0-9]+):([0-9]+):([0-9]+)" #without microSecs
                    m = re.match(pattern, string)
                    [hours, mins, secs] = [int(x) for x in m.groups()[1:]]
                    microSecs = 0
                    sign = m.groups()[0]
                    if sign: positive = False
                except Exception:
                    print("Error trying to parse " + string)
        self.positive = positive
        self.hours = hours
        self.mins = mins
        self.secs = secs
        self.microSecs = microSecs
        self._calc()
    
    def getString(self):
        string = ""
        for x in [self.hours, self.mins, self.secs]:
            string += str(x).rjust(2, "0") + ":"
        string = string[:-1] + "," + str(self.microSecs).rjust(3, "0")
        if not self.positive:
            string = "-" + string
        return string        
    
    def flipSigned(self):
        flipped = SrtTime(self.getString())
        flipped.positive = not flipped.positive
        return flipped
    
    def _length(self):
        return self.microSecs/1000 + self.secs + 60 * self.mins + 3600 * self.hours
    
    def __gt__(self, other):
        if self.positive and other.positive:
            return self._length() > other._length()
        elif not self.positive and not other.positive:
            return other._length() > self._length()
        else:
            return self.positive
    
    def __str__(self):
        return self.getString()
        
    def __add__(self, other):
        if self.positive != other.positive: #one of them is negative
            if self.positive:
                return self - other.flipSigned()
            else: #only self is negative
                return other - self.flipSigned()
        else: #both 
            positive = self.positive #sign of sum follows the addend regardless
            hours = self.hours + other.hours
            mins = self.mins + other.mins
            secs = self.secs + other.secs
            microSecs = self.microSecs + other.microSecs
            return SrtTime(hours=hours, mins=mins, secs=secs, microSecs=microSecs, positive=positive)
    
    def __sub__(self, other):
        if self.positive != other.positive: #different signs
            if self.positive:
                return self + other.flipSigned()
            else: #only self is negative
                value = self.flipSigned() + other
                return value.flipSigned()
        elif self.positive: #same signs, both positive
            if self > other:
                positive = self.positive
                hours = self.hours - other.hours
                mins = self.mins - other.mins
                secs = self.secs - other.secs
                microSecs = self.microSecs - other.microSecs
                return SrtTime(hours=hours, mins=mins, secs=secs, microSecs=microSecs, positive=positive) 
            elif other > self:
                value = other - self
                return value.flipSigned()
            else: #equality
                return SrtTime(string="00:00:00,000")
        elif not self.positive: #same signs, both negative (e.g. -3 - (-7) or -4 -(-1))
            return other.flipSigned() - self.flipSigned()
  
    def _calc(self):    
        while self.microSecs < 0:
            self.microSecs += 1000
            self.secs -= 1        
        if self.microSecs >= 1000:
            self.secs += self.microSecs // 1000
            self.microSecs = self.microSecs % 1000
        
        while self.secs < 0:
            self.secs += 60
            self.mins -= 1
        if self.secs >= 60:
            self.mins += self.secs // 60
            self.secs = self.secs % 60
            
        while self.mins < 0:
            self.mins += 60
            self.hours -= 1
        if self.mins >= 60:
            self.hours += self.mins // 60
            self.mins = self.mins % 60
            

class modeException(Exception):
    pass
