class Luhn:
    """
    given a number, assert if it respects the Luhn logic
    """
    def __init__(self, card_num):

        # raise if any non int characters come in the user input;
        # remove any spaces
        try:
            self.card_num = [int(i) for i in card_num.replace(' ', '')]
        except ValueError:
            return False

        pass

    def double_even_pos(self):
        """
        double every second int, starting from the right, and apply the luhn logic
        :return: concatenated list of the doubled even positions and normal odd list positions
        """
        after_double = [i*2 if i*2 < 9 else i * 2 - 9 for i in self.card_num[::-2]]

        return after_double + self.card_num[::2]

    def sum_digits(self):
        return sum(self.double_even_pos())

    def isMultiple(self, multiple):
        return True if not self.sum_digits() % 10 else False

    def valid(self):
        return self.isMultiple(10)


