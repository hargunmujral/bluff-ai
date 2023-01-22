import card_eval
import math

# total number of combos of these hands
TOTALHANDS = 321319656
QUADS = 624
FULLHOUSE = 3744
STRAIGHT = 10200
TRIPS = 122304
TWOPAIR = 134784
PAIR = 9172800
HIGHCARDS = 311875200

# call is a list of Cards
def IV(numCards, call):
    numBeat = 0
    if card_eval.highCard(call):
        print("high card")
        # add in better counting
    elif card_eval.onePair(call):
        print("one pair")
        numBeat = HIGHCARDS
        # add in better counting
    elif card_eval.twoPair(call):
        print("two pair")
        numBeat = HIGHCARDS + PAIR
        # add in better counting
    elif card_eval.threeOfAKind(call):
        print("trips")
        numBeat = HIGHCARDS + PAIR + TWOPAIR
        # add in better counting
    elif card_eval.straight(call):
        print("straight")
        numBeat = HIGHCARDS + PAIR + TWOPAIR + TRIPS
        # add in better counting
    elif card_eval.fullHouse(call):
        print("full house")
        numBeat = HIGHCARDS + PAIR + TWOPAIR + TRIPS + STRAIGHT
        # add in better counting
    else:
        numBeat = HIGHCARDS + PAIR + TWOPAIR + TRIPS + STRAIGHT + FULLHOUSE
        # add in better counting
        print("quads")
    return round(1.0 - float((numBeat/math.factorial(numCards)/TOTALHANDS)), 5)