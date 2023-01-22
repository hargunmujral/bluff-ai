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


class Deck(object):
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
            # print('Hand ' + str(i + 1) + ': ' + hand)

    def startGame(self, hand):
        sortedHand = sorted(hand, reverse=True)
        self.fourOfAKind(sortedHand)

    def fourOfAKind(self, sortedHand):
        mylist = []
        for card in sortedHand:
            mylist.append(card.rank)
        Currank = sortedHand[2].rank
        if mylist.count(Currank) == 4:
            # print('Four of a Kind')
            self.tlist.append(14**6*Currank)
            handsMap['fourOfAKind'] += 1
        else:
            self.fullHouse(sortedHand)

    def fullHouse(self, sortedHand):
        mylist = []
        for card in sortedHand:
            mylist.append(card.rank)
        rank1 = sortedHand[0].rank
        rank2 = sortedHand[-1].rank
        num_rank1 = mylist.count(rank1)
        num_rank2 = mylist.count(rank2)
        if (num_rank1 == 2 and num_rank2 == 3):
            # print('Full House')
            self.tlist.append(14**5*rank2 + rank1) 
            handsMap['fullHouse'] += 1
        elif (num_rank1 == 3 and num_rank2 == 2):
            # print('Full House')
            self.tlist.append(14**5*rank1 + rank2)
            handsMap['fullHouse'] += 1
        else:
            self.straight(sortedHand)

    lowStraight = [14, 5, 4, 3, 2]
    def straight(self, sortedHand):
        if [card.rank for card in sortedHand] == self.lowStraight:
            # print('Straight')
            self.tlist.append(14**4*5)
            handsMap['straight'] += 1
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
            # print('Straight')
            self.tlist.append(14**4*Currank)
            handsMap['straight'] += 1
        else:
            self.threeOfAKind(sortedHand)

    def threeOfAKind(self, sortedHand):
        Currank = sortedHand[2].rank
        mylist = []
        for card in sortedHand:
            mylist.append(card.rank)
        if mylist.count(Currank) == 3:
            # print("Three of a Kind")
            self.tlist.append(14**3*Currank)
            handsMap['threeOfAKind'] += 1
        else:
            self.twoPair(sortedHand)

    def twoPair(self, sortedHand):
        rank1 = sortedHand[1].rank
        rank2 = sortedHand[3].rank
        mylist = []
        for card in sortedHand:
            mylist.append(card.rank)
        if mylist.count(rank1) == 2 and mylist.count(rank2) == 2:
            # print("Two Pair")
            self.tlist.append(14**2*max(rank1, rank2))
            handsMap['twoPair'] += 1
        else:
            self.onePair(sortedHand)

    def onePair(self, sortedHand):
        mylist = defaultdict(int)
        for card in sortedHand:
            mylist[card.rank] += 1
        for rank, count in mylist.items():
          if count == 2:
            self.tlist.append(14*rank)
            handsMap['onePair'] += 1
            return
        self.highCard(sortedHand)

    def highCard(self, sortedHand):
        mylist = []
        for card in sortedHand:
            mylist.append(card.rank)
        # print("High Card")
        self.tlist.append(sortedHand[0].rank)
        handsMap['highCard'] += 1


def main():
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

    maxpoint = max(game.tlist)
    maxindex = game.tlist.index(maxpoint)

    print('\nHand %d wins' % (maxindex+1))


def runRandomGames():
    game = Poker(1)
    game.play()
    game.startGame(game.hands[0])


handsMap = {'fourOfAKind': 0, 'fullHouse': 0, 'straight': 0,
            'threeOfAKind': 0, 'twoPair': 0, 'onePair': 0, 'highCard': 0}


def handPercentage(runs):
    for key in handsMap:
        handsMap[key] = handsMap[key] / runs
        print(key, handsMap[key])


# main()

def simulation(runs=100000):

    for i in range(runs):
        runRandomGames()

    handPercentage(runs)
    print(handsMap)


simulation()

# output observed (very very close to expected!!!!)

# {'fourOfAKind': 0.0002, 'fullHouse': 0.0012, 'straight': 0.0045,
#     'threeOfAKind': 0.0195, 'twoPair': 0.0485, 'onePair': 0.4238, 'highCard': 0.5023}