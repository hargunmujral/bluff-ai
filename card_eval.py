import random
from collections import defaultdict


class Card(object):
    RANKS = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)

    def __init__(self, rank):
        self.rank = rank

    def __str__(self):
        if self.rank == 14:
            rank = 'A'
        elif self.rank == 13:
            rank = 'K'
        elif self.rank == 12:
            rank = 'Q'
        elif self.rank == 11:
            rank = 'J'
        else:
            rank = self.rank
        return str(rank)

    def __eq__(self, other):
        return (self.rank == other.rank)

    def __ne__(self, other):
        return (self.rank != other.rank)

    def __lt__(self, other):
        return (self.rank < other.rank)

    def __le__(self, other):
        return (self.rank <= other.rank)

    def __gt__(self, other):
        return (self.rank > other.rank)

    def __ge__(self, other):
        return (self.rank >= other.rank)


class Deck (object):
    def __init__(self):
        self.deck = []
        for rank in 4*Card.RANKS:
            card = Card(rank)
            self.deck.append(card)

    def shuffle(self):
        random.shuffle(self.deck)

    def __len__(self):
        return len(self.deck)

    def deal(self):
        if len(self) == 0:
            return None
        else:
            return self.deck.pop(0)


class Poker(object):
    def __init__(self, numHands):
        self.deck = Deck()
        self.deck.shuffle()
        self.hands = []
        self.tlist = []
        numCards_in_Hand = 5

        for _ in range(numHands):
            hand = []
            for _ in range(numCards_in_Hand):
                hand.append(self.deck.deal())
            self.hands.append(hand)

    def play(self):
        for i in range(len(self.hands)):
            sortedHand = sorted(self.hands[i], reverse=True)
            hand = ''
            for card in sortedHand:
                hand = hand + str(card) + ' '
            print('Hand ' + str(i + 1) + ': ' + hand)

    def startGame(self, hand):
        sortedHand = sorted(hand, reverse=True)
        self.fourOfAKind(sortedHand)

    def fourOfAKind(self, hand):
        sortedHand = sorted(hand, reverse=True)
        mylist = []
        for card in sortedHand:
            mylist.append(card.rank)
        Currank = sortedHand[2].rank
        if mylist.count(Currank) == 4:
            print('Four of a Kind')
            self.tlist.append(14**6*Currank)
        else:
            self.fullHouse(sortedHand)

    def fullHouse(self, hand):
        sortedHand = sorted(hand, reverse=True)
        mylist = []
        for card in sortedHand:
            mylist.append(card.rank)
        rank1 = sortedHand[0].rank
        rank2 = sortedHand[-1].rank
        num_rank1 = mylist.count(rank1)
        num_rank2 = mylist.count(rank2)
        if (num_rank1 == 2 and num_rank2 == 3):
            print('Full House')
            self.tlist.append(14**5*rank2 + rank1) 
        elif (num_rank1 == 3 and num_rank2 == 2):
            print('Full House')
            self.tlist.append(14**5*rank1 + rank2)
        else:
            self.straight(sortedHand)
    lowStraight = [14, 5, 4, 3, 2]
    def straight(self, hand):
        sortedHand = sorted(hand, reverse=True)
        if [card.rank for card in sortedHand] == self.lowStraight:
            # print('Straight')
            self.tlist.append(14**4*5)
            return
        flag = True
        Currank = sortedHand[0].rank
        for card in sortedHand:
            if card.rank != Currank:
                flag = False
                break
            else:
                Currank -= 1
        if flag:
            print('Straight')
            self.tlist.append(14**4*Currank)
        else:
            self.threeOfAKind(sortedHand)

    def threeOfAKind(self, hand):
        sortedHand = sorted(hand, reverse=True)
        Currank = sortedHand[2].rank
        mylist = []
        for card in sortedHand:
            mylist.append(card.rank)
        if mylist.count(Currank) == 3:
            print("Three of a Kind")
            self.tlist.append(14**3*Currank)
        else:
            self.twoPair(sortedHand)

    def twoPair(self, hand):
        sortedHand = sorted(hand, reverse=True)
        rank1 = sortedHand[1].rank
        rank2 = sortedHand[3].rank
        mylist = []
        for card in sortedHand:
            mylist.append(card.rank)
        if mylist.count(rank1) == 2 and mylist.count(rank2) == 2:
            print("Two Pair")
            self.tlist.append(14**2*max(rank1, rank2))
        else:
            self.onePair(sortedHand)

    def onePair(self, hand):
        sortedHand = sorted(hand, reverse=True)
        mylist = defaultdict(int)
        for card in sortedHand:
            mylist[card.rank] += 1
        for rank, count in mylist.items():
          if count == 2:
            self.tlist.append(14*rank)
            return
        self.highCard(sortedHand)

    def highCard(self, hand):
        sortedHand = sorted(hand, reverse=True)
        mylist = []
        for card in sortedHand:
            mylist.append(card.rank)
        print("High Card")
        self.tlist.append(sortedHand[0].rank)


def matchup():
    numHands = eval(input('Enter number of hands to play: '))
    while (numHands < 2 or numHands > 6):
        numHands = eval(input('Enter number of hands to play: '))
    game = Poker(numHands)
    game.play()

    print('\n')
    for i in range(numHands):
        curHand = game.hands[i]
        print("Hand " + str(i+1) + ": ", end="")
        game.startGame(curHand)
    print(game.tlist)
    maxpoint = max(game.tlist)
    maxindex = game.tlist.index(maxpoint)

    print('\nHand %d wins' % (maxindex+1))

def customMatchup():
    num = int(input('Enter number of hands: '))
    hands = []
    for i in range(num):
      hand = []
      print('Enter cards for hand %d' % (i+1))
      for i in range(5):
          card = input('Enter card: ')
          rank = detectRank(card)
          hand.append(Card(rank))
      hands.append(hand)

    numHands = len(hands)
    game = Poker(numHands)
    # game.play()

    print('\n')
    for i, hand in enumerate(hands):
        print("Hand " + str(i+1) + ": ", end="")
        game.startGame(hand)
    print(game.tlist)
    maxpoint = max(game.tlist)
    maxindex = game.tlist.index(maxpoint)

    print('\nHand %d wins' % (maxindex+1))


def detectRank(card):
    if card == "A":
        return 14
    elif card == "K":
        return 13
    elif card == "Q":
        return 12
    elif card == "J":
        return 11
    # check between 2 and 10
    elif 2 <= int(card) <= 10:
        return int(card)
    else:
        # throw exception
        raise Exception("Invalid card")


def checkCustomHand(num):
    hand = []
    for i in range(num):
        card = input('Enter card: ')
        rank = detectRank(card)
        hand.append(Card(rank))
    game = Poker(1)
    game.startGame(hand)
