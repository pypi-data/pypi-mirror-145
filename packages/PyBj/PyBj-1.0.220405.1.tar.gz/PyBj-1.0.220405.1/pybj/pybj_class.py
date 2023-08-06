import os
from random import shuffle

class game_deck:
    def __init__(self, deck_set = 6):
        self.card_suit = ["♣", "♦", "♥", "♠"]
        self.card_rank = {" 2":2, " 3":3, " 4":4, " 5":5, " 6":6,
                          " 7":7, " 8":8, " 9":9, "10":10, " J":10,
                          " Q":10, " K":10, " A":11}
        self.card_deck = []
        for _ in range(0, deck_set):
            for suit in self.card_suit:
                for rank in self.card_rank:
                    self.card_deck.append([f"[ {rank} of {suit} ]", self.card_rank[rank]])
        shuffle(self.card_deck)

    def draw(self):
        remove_card = self.card_deck[-1]
        self.card_deck.pop()
        return {remove_card[0]:remove_card[1]}

class game_chip:
    def __init__(self):
        self.chip_value = {1:1, 2:5, 3:25, 4:50, 5:100, 6:500}
        self.chip_color = {1:"White Chip  ($1)", 2:"Red Chip    ($5)", 3:"Green Chip  ($25)",
                           4:"Orange Chip ($50)", 5:"Black Chip  ($100)", 6:"Purple Chip ($500)"}

    def value(self):
        return self.chip_value

    def color(self, chip_option):
        return self.chip_color[chip_option]

class game_calculator:
    def __init__(self, number):
        self.number = number

    def insurance(self):
        self.number /= 2
        return float(self.number)

    def insurance_payout(self):
        self.number = 2 * (self.number / 1)
        return float(self.number)

    def blackjack_payout(self):
        self.number = 3 * (self.number / 2)
        return float(self.number)

    def win_payout(self):
        self.number = self.number * 2
        return float(self.number)

    def double_down(self):
        self.number += self.number
        return float(self.number)

    def surrender(self):
        self.number = self.number / 2
        return float(self.number)

    def hand_value(self):
        hand_total = 0
        for card_value in self.number:
            hand_total += card_value
        return hand_total

class game_safe:
    def __init__(self, player_money):
        self.player_money = player_money

    def deposit(self, player_bet):
        self.player_money += player_bet

    def withdraw(self, player_bet):
        self.player_money -= player_bet

    def balance(self):
        return float(self.player_money)

class game_hand:
    def __init__(self):
        self.card_pattern = []
        self.card_value = []

    def draw_card(self, draw_deck):
        [(key, value)] = draw_deck.items()
        self.card_pattern.append(key)
        self.card_value.append(value)
        return value

    def split_hand(self):
        split_card = {self.card_pattern[-1]:self.card_value[-1]}
        self.card_pattern.pop()
        self.card_value.pop()
        return split_card

    def pattern(self):
        return self.card_pattern

    def value(self):
        return self.card_value

class game_log:
    def __init__(self, player_status, player_money, player_bet, player_insurance = ""):
        self.player_status = player_status
        self.player_money = player_money
        self.player_bet = player_bet
        self.player_insurance = player_insurance

    def __str__(self):
        if bool(self.player_insurance):
            return (f"Status   : {self.player_status}\n"
                    f"Wallet   : ${self.player_money}\n"
                    f"Bet      : ${self.player_bet}\n"
                    f"Insurance: {self.player_insurance}")
        else:
            return (f"Status   : {self.player_status}\n"
                    f"Wallet   : ${self.player_money}\n"
                    f"Bet      : ${self.player_bet}")

class game_table:
    def __init__(self, hand_card):
        self.hand_card = hand_card

    def facedown(self, print_output = True):
        if print_output:
            print("\nDealer's hand", flush = True)
            print("=" * 13, flush = True)
            for pattern in [self.hand_card.pattern()[0], "[Face-down]"]:
                print(f"{pattern}", flush = True)
        hand_value = game_calculator(self.hand_card.value()).hand_value()
        if (11 in self.hand_card.value()) and (hand_value > 21):
            hand_value = game_calculator([1 if number == 11 else number for number in self.hand_card.value()]).hand_value() + 10
        if self.hand_card.value()[0] != 11:
            if print_output:
                print(f"Total: {self.hand_card.value()[0]}", flush = True)
            return hand_value, False
        else:
            return hand_value, True

    def faceup(self, hand_owner, hand_number = None, hand_result = "", print_output = True):
        if print_output:
            if hand_number != None:
                print(f"\n{hand_owner}'s {hand_number}-hand", flush = True)
                print("=" * 17, flush = True)
            else:
                print(f"\n{hand_owner}'s hand", flush = True)
                print("=" * 13, flush = True)
            for pattern in self.hand_card.pattern():
                print(f"{pattern}", flush = True)
        hand_value = game_calculator(self.hand_card.value()).hand_value()
        if (11 in self.hand_card.value()) and (hand_value > 21):
            hand_value = game_calculator([1 if number == 11 else number for number in self.hand_card.value()]).hand_value() + 10
            if hand_value > 21:
                hand_value -= 10
        if print_output:
            print(f"Total: {hand_value}", flush = True)
        if bool(hand_result):
            print(f"Result: {hand_result}", flush = True)
        return hand_value

class refresh_screen:
    def __init__(self):
        os.system('cls' if os.name == 'nt' else 'clear')