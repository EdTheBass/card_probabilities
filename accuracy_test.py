from random import randint
import card_probability

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

deck = ["" for x in range(52)]

correct_sum = 0
tests = 0
minimum = 52
maximum = 0

def scramble():
    global deck

    deck = ["" for x in range(52)]

    for card in DECK_CONST:
        index = randint(0, 51)

        while deck[index]:
            index = randint(0, 51)

        deck[index] = card

def play():
    global correct_sum, tests, minimum, maximum

    correct = card_probability.play_comp_deck(deck)
    if correct < minimum:
        minimum = correct
    elif correct > maximum:
        maximum = correct

    correct_sum += correct
    tests += 1

for x in range(1000):
    scramble()
    play()

print(f"{correct_sum/tests} average correct")
print(f"{minimum} minimum")
print(f"{maximum} maximum")