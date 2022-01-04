import random

DECK_CONST = ["a", "a", "a", "a",
              "2", "2", "2", "2",
              "3", "3", "3", "3",
              "4", "4", "4", "4",
              "5", "5", "5", "5",
              "6", "6", "6", "6",
              "7", "7", "7", "7",
              "8", "8", "8", "8",
              "9", "9", "9", "9",
              "10", "10", "10", "10",
              "j", "j", "j", "j",
              "q", "q", "q", "q",
              "k", "k", "k", "k"]

deck = DECK_CONST[:]

cards = ["a", "2", "3", "4", "5", "6", "7", "8", "9", "10", "j", "q", "k"]
correct = 0
prev = ""

def shuffle():
    global deck

    deck = ["" for x in range(52)]
    for card in DECK_CONST:
        index = random.randint(0, 51)
        while deck[index]:
            index = random.randint(0, 51)
        deck[index] = card

def card_shown(comp_data=""):
    global correct

    if not comp_data:
        while True:
            card = input("Card: ").strip().lower()

            if card == "end":
                return -1

            if card not in cards or card not in deck:
                print("Invalid card.")
                continue

            break
    else:
        card = comp_data

    if card == prev:
        correct += 1
    deck.remove(card)

def calc_prob():
    global prev

    def _max(array):
        index = 0
        highest = 0
        for x in range(len(array)):
            if array[x] > highest:
                highest = array[x]
                index = x
        return [highest, index]

    occurences = [0 for z in range(13)]
    for card in deck:
        occurences[cards.index(card)] += 1

    most_common_range = []
    for y in range(len(cards)):
        if occurences[y] == _max(occurences)[0]:
            most_common_range.append(cards[y])

    most_common = cards[_max(occurences)[1]]

    occurences.sort()
    probability = occurences[-1] / len(deck)

    prev = most_common

    return [most_common, probability]


def play_input():
    global deck, correct, prev

    while True:
        if len(deck) == 1:
            deck = DECK_CONST[:]
            print(f"Scrambled. Correct {correct} times.\n")
            correct = 0
            prev = ""

        card_shown()
        prob = calc_prob()
        print(f"{prob[0]} at {prob[1]*100:0.1f}%\n")


def play_comp_deck(data):
    global deck, correct, prev

    correct = 0
    prev = ""

    counter = 0
    while True:
        if len(deck) == 1:
            deck = DECK_CONST[:]
            return correct

        card_shown(data[counter])
        prob = calc_prob()

        counter += 1

def play_comp_card(card):
    global deck, correct, prev

    if card == "start":
        correct = 0
        prev = ""
        return

    elif card == "end":
        deck = DECK_CONST[:]
        return

    card_shown(card)

if __name__ == "__main__":
    mode = play_input if input("Mode: ").strip().lower() == "y" else play_comp_deck

    mode()
