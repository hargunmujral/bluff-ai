import card_eval as ce

def main():
    choice = input('Enter 1 to play a game, 2 to check a custom hand, 3 to play with local player(s): ')
    if choice == '1':
        ce.matchup()
    elif choice == '2':
        numOfCards = int(input('Enter number of cards: '))
        if (numOfCards > 52 or numOfCards < 1):
            print('Invalid choice')
        ce.checkCustomHand(numOfCards)
    elif choice == '3':
        ce.customMatchup()
    else:
        print('Invalid choice')
