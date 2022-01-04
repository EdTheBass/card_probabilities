import card_probability
import basic_strategy

values = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "a": 11,
    "j": 10,
    "q": 10,
    "k": 10
}

class Dealer:
    def __init__(self):
        self.hand = []
        self.total = 0
        self.a_count = 0

    def eval_total(self):
        self.total = 0

        for _card in self.hand:
            val = values.get(_card)
            self.total += val

        while self.total > 21 and self.a_count != 0:
            self.total -= 10


    def play(self):
        while True:
            self.eval_total()
            if self.total < 17:
                self.hit()
                return 0
            else:
                return 1

    def hit(self):
        _card = card_probability.calc_prob()[0]
        if _card == "a":
            self.a_count += 1
        self.hand.append(_card)

        input_card(_card)

class Player:
    def __init__(self):
        self.hands = [[]]
        self.total = 0
        self.a_count = 0

    def eval_total(self, _hand):
        self.total = 0

        for _card in self.hands[_hand]:
            val = values.get(_card)
            self.total += val

        while self.total > 21 and self.a_count != 0:
            self.total -= 10

    def play(self, upcard, _hand):
        if upcard in ["j", "q", "k"]:
            upcard = "10"
        action_index = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "a"].index(upcard)

        self.eval_total(_hand)

        if len(self.hands[_hand]) == 1:
            self.hit(_hand)
            return 0

        if "a" not in self.hands[_hand]:
            hard_soft = "h"
        else:
            hard_soft = "s"

        if self.hands[_hand][0] == self.hands[_hand][1]:
            split = "d"
        else:
            split = ""

        if split:
            action = basic_strategy.basic_strat.get((self.total, split, hard_soft))[action_index]
        else:
            action = basic_strategy.basic_strat.get((self.total, hard_soft))[action_index]

        if action == "h":
            self.hit(_hand)
            return 0
        elif action == "s":
            return 1
        elif action == "d":
            self.double(_hand)
            return 2
        elif action == "su":
            return 3
        elif action == "sp":
            self.split(_hand)
            return 4
        elif action == "ds":
            if len(self.hands[_hand]) > 2:
                return
            else:
                self.double(_hand)
                return 2

    def hit(self, _hand):
        _card = card_probability.calc_prob()[0]
        if _card == "a":
            self.a_count += 1
        self.hands[_hand].append(_card)

        input_card(_card)

    def double(self, _hand):
        # exists in case i implement betting, not yet though
        self.hit(_hand)

    def split(self, _hand):
        self.hands[_hand] = self.hands[_hand][:1]
        self.hands.append([self.hands[_hand][0]])
        self.hit(_hand)


def deal(_dealer, _player):
    _dealer.hand = []
    _player.hands = [[]]
    _dealer.hit()
    _dealer.hit()
    _player.hit(0)
    _player.hit(0)

def input_card(_card):
    card_probability.play_comp_card(_card)

dealer = Dealer()
player = Player()

while True:
    input_card("start")

    while True:
        if card_probability.card_shown() == -1:
            break

    print()

    deal(dealer, player)
    p_hand = 0

    for card in dealer.hand:
        input_card(card)
    for card in player.hands[0]:
        input_card(card)

    card_probability.deck[0] = "a"
    card_probability.deck[-1] = "2"

    while True:
        try:
            player_go = player.play(dealer.hand[0], p_hand)
        except IndexError:
            break

        if player_go == 0:
            print("Player hit")
            continue
        elif player_go == 1:
            print("Player stood")
            if len(player.hands) > 1:
                p_hand += 1
                continue
            break
        elif player_go == 2:
            print("Player doubled")
            break
        elif player_go == 3:
            print("Player surrendered")
            break
        elif player_go == 4:
            print("Player split")
            continue

    print()
    while True:
        dealer_go = dealer.play()

        if dealer_go == 0:
            print("Dealer hit")
            continue
        elif dealer_go == 1:
            print("Dealer stood")
            break

    print()
    dealer.eval_total()
    for hand in range(len(player.hands)):
        player.eval_total(hand)
        if player.total > 21 or player.total < dealer.total < 21:
            print(f"Player lost on hand {hand+1}")
            continue
        elif player.total == dealer.total:
            print(f"Player pushed on hand {hand+1}")
            continue
        else:
            print(f"Player won on hand {hand+1}")
            continue

    input_card("end")

    break

print(dealer.hand)
print(dealer.total)

print()
for _hand_ in range(len(player.hands)):
    player.eval_total(_hand_)
    print(player.hands[_hand_])
    print(player.total)
