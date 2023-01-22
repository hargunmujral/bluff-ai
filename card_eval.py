import random


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


class Poker (object):
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

    def point(self, hand):
        sortedHand = sorted(hand, reverse=True)
        c_sum = 0
        ranklist = []
        for card in sortedHand:
            ranklist.append(card.rank)
        c_sum = ranklist[0]*13**4+ranklist[1]*13**3 + \
            ranklist[2]*13**2+ranklist[3]*13+ranklist[4]
        return c_sum

    def startGame(self, hand):
        sortedHand = sorted(hand, reverse=True)
        self.fourOfAKind(sortedHand)

    def fourOfAKind(self, hand):
        sortedHand = sorted(hand, reverse=True)
        h = 8
        Currank = sortedHand[1].rank
        count = 0
        total_point = h*13**5+self.point(sortedHand)
        for card in sortedHand:
            if card.rank == Currank:
                count += 1
        if not count < 4:
            print('Four of a Kind')
            self.tlist.append(total_point)
        else:
            self.fullHouse(sortedHand)

    def fullHouse(self, hand):
        sortedHand = sorted(hand, reverse=True)
        h = 7
        total_point = h*13**5+self.point(sortedHand)
        mylist = []
        for card in sortedHand:
            mylist.append(card.rank)
        rank1 = sortedHand[0].rank
        rank2 = sortedHand[-1].rank
        num_rank1 = mylist.count(rank1)
        num_rank2 = mylist.count(rank2)
        if (num_rank1 == 2 and num_rank2 == 3) or (num_rank1 == 3 and num_rank2 == 2):
            print('Full House')
            self.tlist.append(total_point)
        else:
            self.straight(sortedHand)

    def straight(self, hand):
        sortedHand = sorted(hand, reverse=True)
        flag = True
        h = 5
        total_point = h*13**5+self.point(sortedHand)
        Currank = sortedHand[0].rank
        for card in sortedHand:
            if card.rank != Currank:
                flag = False
                break
            else:
                Currank -= 1
        if flag:
            print('Straight')
            self.tlist.append(total_point)

        else:
            self.threeOfAKind(sortedHand)

    def threeOfAKind(self, hand):
        sortedHand = sorted(hand, reverse=True)
        h = 4
        total_point = h*13**5+self.point(sortedHand)
        Currank = sortedHand[2].rank
        mylist = []
        for card in sortedHand:
            mylist.append(card.rank)
        if mylist.count(Currank) == 3:
            print("Three of a Kind")
            self.tlist.append(total_point)

        else:
            self.twoPair(sortedHand)

    def twoPair(self, hand):
        sortedHand = sorted(hand, reverse=True)
        h = 3
        total_point = h*13**5+self.point(sortedHand)
        rank1 = sortedHand[1].rank
        rank2 = sortedHand[3].rank
        mylist = []
        for card in sortedHand:
            mylist.append(card.rank)
        if mylist.count(rank1) == 2 and mylist.count(rank2) == 2:
            print("Two Pair")
            self.tlist.append(total_point)

        else:
            self.onePair(sortedHand)

    def onePair(self, hand):
        sortedHand = sorted(hand, reverse=True)
        h = 2
        total_point = h*13**5+self.point(sortedHand)
        mylist = []
        mycount = []
        for card in sortedHand:
            mylist.append(card.rank)
        for each in mylist:
            count = mylist.count(each)
            mycount.append(count)
        if mycount.count(2) == 2 and mycount.count(1) == 3:
            print("One Pair")
            self.tlist.append(total_point)
        else:
            self.highCard(sortedHand)

    def highCard(self, hand):
        sortedHand = sorted(hand, reverse=True)
        h = 1
        total_point = h*13**5+self.point(sortedHand)
        mylist = []
        for card in sortedHand:
            mylist.append(card.rank)
        print("High Card")
        self.tlist.append(total_point)


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


# main()

# checkCustomHand()

def main():
    choice = input('Enter 1 to play a game or 2 to check a custom hand: ')
    if choice == '1':
        matchup()
    elif choice == '2':
        numOfCards = int(input('Enter number of cards: '))
        if (numOfCards > 52 or numOfCards < 1):
            print('Invalid choice')
        checkCustomHand(numOfCards)
    else:
        print('Invalid choice')


main()
