from random import shuffle
from random import randrange
from queries import get_places
#given trip id, get all placeNames of the trip into places array
#places = ["Zara", "Adigas", "Bangalore Central", "City Bar", "Drinks on MG", "Ebony", "Forum", "Garuda", "Hundred Ft", "Indigo Live Music Bar", "Jawaharlal Nehru Planetarium", "Kobes", "Little Italy", "Mamagoto", "War Memorial Park", "Olive Beach"]

def get_diary(places):

    fillFirstSentence = ["I had a wonderful trip. ", "Let me tell you about my trip. ", "I visited a lot of interesting places. "]

    fillersDouble = ["I visited {0} and {1}. ", "I saw {0} and {1}. ", "{0} was great but {1} shouldn't be missed. ", "{0} and {1} were nice. "]
    fillersSingle = [ "My favourite was {0}. ", "I had a lot of fun at {0}. ", "Seeing {0} was a highlight. ", "I will definitely visit {0} again. ", "{0} was the best. ", "You'll all enjoy visiting {0} for sure. ", "{0} is spectacular. "]

    fillLastSentence = ["You should be sure to visit these places too", "This trip was a lot of fun", "I will definitely do this again soon"]

    shuffle(fillFirstSentence)
    shuffle(fillersDouble)
    shuffle(fillersSingle)
    shuffle(fillLastSentence)
    shuffle(places)

    pos = 0
    singlePos = 0
    doublePos = 0
    abandon = False

    res = fillFirstSentence[0]

    """
        while at least two places left
        if there are both single and double strings left
        pick one randomly
        else if there are single strings left
        pick a single string
        else if there are double strings left
        pick a double string
        else if nothing left
        abandon rest of the places
    """
    while pos < len(places) - 1:
        if (singlePos < len(fillersSingle)) and (doublePos < len(fillersDouble)):
            i = randrange(0, 2)
            if i == 0: #single
                res += fillersSingle[singlePos].format(places[pos])
                singlePos += 1
                pos += 1
            else:
                res += fillersDouble[doublePos].format(places[pos], places[pos + 1])
                doublePos += 1
                pos += 2
        elif singlePos < len(fillersSingle):
            res += fillersSingle[singlePos].format(places[pos])
            singlePos += 1
            pos += 1
        elif doublePos < len(fillersDouble):
            res += fillersDouble[doublePos].format(places[pos], places[pos + 1])
            doublePos += 1
            pos += 2
        else:
            abandon = True
            pos = len(places)

    if pos == len(places) - 1 or abandon:
        res += "There were some other nice places as well. "

    res += fillLastSentence[0]
    return res
	
if __name__ == "__main__":
    res = get_diary(places)
    print(res)
