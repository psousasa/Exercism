start = """On the {} day of Christmas my true love gave to me:"""

day = ['first', 'second', 'third', 'forth',
       'fifth', 'sixth', 'seventh', 'eighth', 'nineth', 'tenth', 'eleventh', 'twelfth']

end = """twelve Drummers Drumming
eleven Pipers Piping
ten Lords-a-Leaping
nine Ladies Dancing
eight Maids-a-Milking
seven Swans-a-Swimming
six Geese-a-Laying
five Gold Rings
four Calling Birds
three French Hens
two Turtle Doves
a Partridge in a Pear Tree.""".split('\n')




def recite(start_verse, end_verse):
    """
    join the several parts of each accruing verse from the twelve days carol
    :param start_verse: int - first verse to consider
    :param end_verse: int - last verse to consider
    :return: list of verses considered
    """

    carol = []

    for day_nb in range(start_verse-1, end_verse):  # -1 to accommodate python index logic"

        if day_nb == 0:  # if first day - avoid adding and
            phrase = ' '.join([start.format(day[day_nb]), end[-1]])

        else:
            phrase = ', '.join(end[-(day_nb+1):-1])  # join each day present
            phrase = ', and '.join([phrase, end[-1]])  # join the last day present - separate because of and
            phrase = ' '.join([start.format(day[day_nb]), phrase])  # join the start of the verse

        carol.append(phrase)

    return carol
