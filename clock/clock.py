class Clock:
    """
    create clock that allows hh:mm representation and is 00:00 at midnight.
    Working 24h.
    allows adding and subtracting minutes
    allows clock comparisons on str repr
    assumes positive time input
    """
    def __init__(self, hour, minute):
        """
        create minutes and hours, with only relevant entries
        :param hour: add hours to any hour converted from minutes
        :param minute: keep only relevant minutes
        """
        self.minute = minute % 60

        self.hour = (hour + (minute // 60)) % 24

        pass

    def __repr__(self):
        """

        :return: pad with an extra zero in case len = 1
        """
        return f'{self.hour:02}:{self.minute:02}'

    def __eq__(self, other):
        return str(self) == str(other)

    def __add__(self, minutes):
        return Clock(self.hour, self.minute + minutes)

    def __sub__(self, minutes):
        return Clock(self.hour, self.minute - minutes)

