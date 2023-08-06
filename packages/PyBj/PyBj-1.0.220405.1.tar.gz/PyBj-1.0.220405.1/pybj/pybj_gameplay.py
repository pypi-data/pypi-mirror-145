import sys
from time import sleep
from .pybj_class import *

def game_play(player_status, player_wallet, player_deal):
    blackjack_deck = game_deck()
    dealer_hand = game_hand()
    player_hand = game_hand()
    insurance_take = None
    split_card = None
    total_hand = 1
    player_stand = False
    player_quit = False
    # Initial draw
    for _ in list(range(0, 2)):
        player_hand.draw_card(blackjack_deck.draw())
        dealer_hand.draw_card(blackjack_deck.draw())
    dealer_value, insurance_offer = game_table(dealer_hand).facedown(False)
    player_value = game_table(player_hand).faceup(hand_owner = "Player", print_output = False)
    # Insurance offer
    if insurance_offer:
        insurance_deal = game_calculator(player_deal.balance()).insurance()
        if insurance_deal <= player_wallet.balance():
            insurance_payment = 0
            player_insurance = "Deciding"
            while True:
                print(game_log(player_status, player_wallet.balance(), player_deal.balance(), player_insurance), flush = True)
                game_table(dealer_hand).facedown()
                game_table(player_hand).faceup("Player")
                player_decision = input("\nDo you want to take an insurance (Y or N)? ")
                if player_decision.upper() == "Y":
                    insurance_take = True
                    insurance_payment += insurance_deal
                    player_wallet.withdraw(insurance_payment)
                    player_deal.deposit(insurance_payment)
                    player_insurance = "Yes"
                    refresh_screen()
                    break
                elif player_decision.upper() == "N":
                    insurance_take = False
                    player_insurance = "No"
                    refresh_screen()
                    break
                else:
                    player_status = "Wrong input!"
                    refresh_screen()
                    continue
            player_status = "Playing"
    # Split offer
    if player_hand.value()[0] == player_hand.value()[-1]:
        split_deal = 0
        if insurance_take:
            split_deal += player_deal.balance() - insurance_payment
        else:
            split_deal += player_deal.balance()
        if insurance_take != None:
            refresh_screen()
            print(game_log(player_status, player_wallet.balance(), player_deal.balance(), player_insurance), flush = True)
        else:
            print(game_log(player_status, player_wallet.balance(), player_deal.balance()), flush = True)
        game_table(dealer_hand).facedown()
        game_table(player_hand).faceup("Player")
        while (total_hand < 4) and (split_deal <= player_wallet.balance()):
            if total_hand >= 2:
                if insurance_take != None:
                    print(game_log(player_status, player_wallet.balance(), player_deal.balance(), player_insurance), flush = True)
                else:
                    print(game_log(player_status, player_wallet.balance(), player_deal.balance()), flush = True)
                game_table(dealer_hand).facedown()
                game_table(player_hand).faceup("Player", "1st")
                game_table(second_hand).faceup("Player", "2nd")
                if total_hand == 3:
                    game_table(third_hand).faceup("Player", "3rd")
            if total_hand == 1:
                present_hand = "your hand"
            elif total_hand == 2:
                present_hand = "the 2nd-hand"
            elif total_hand == 3:
                present_hand = "the 3rd-hand"
            player_decision = input(f"\nDo you want to split {present_hand} (Y or N)? ")
            if player_decision.upper() == "Y":
                split_card = True
                player_status = "Playing"
                player_wallet.withdraw(split_deal)
                player_deal.deposit(split_deal)
                if total_hand == 1:
                    total_hand += 1
                    second_hand = game_hand()
                    second_hand.draw_card(player_hand.split_hand())
                    second_hand.draw_card(blackjack_deck.draw())
                    refresh_screen()
                    if second_hand.value()[0] == second_hand.value()[-1]:
                        continue
                    else:
                        break
                elif total_hand == 2:
                    total_hand += 1
                    third_hand = game_hand()
                    third_hand.draw_card(second_hand.split_hand())
                    third_hand.draw_card(blackjack_deck.draw())
                    refresh_screen()
                    if third_hand.value()[0] == third_hand.value()[-1]:
                        continue
                    else:
                        break
                elif total_hand == 3:
                    total_hand += 1
                    fourth_hand = game_hand()
                    fourth_hand.draw_card(third_hand.split_hand())
                    fourth_hand.draw_card(blackjack_deck.draw())
                    refresh_screen()
                    continue
            elif player_decision.upper() == "N":
                if total_hand == 1:
                    split_card = False
                refresh_screen()
                break
            else:
                player_status = "Wrong input!"
                refresh_screen()
                if total_hand == 1:
                    if insurance_take != None:
                        print(game_log(player_status, player_wallet.balance(), player_deal.balance(), player_insurance), flush = True)
                    else:
                        print(game_log(player_status, player_wallet.balance(), player_deal.balance()), flush = True)
                    game_table(dealer_hand).facedown()
                    game_table(player_hand).faceup("Player")
                continue
        else:
            refresh_screen()
        player_status = "Playing"
    # Blackjack happens
    if player_value == 21 and not split_card:
        if dealer_value == 21:
            player_status = "Push!"
            if insurance_take:
                player_insurance = "Win!"
                player_wallet.deposit(game_calculator(insurance_payment).insurance_payout())
            player_wallet.deposit(player_deal.balance())
        else:
            player_status = "Blackjack!"
            if insurance_take:
                player_insurance = "Lose!"
                player_deal.withdraw(insurance_payment)
            player_wallet.deposit(player_deal.balance())
            player_wallet.deposit(game_calculator(player_deal.balance()).blackjack_payout())
        player_deal.withdraw(player_deal.balance())
    # Split game
    elif total_hand > 1:
        player_split = total_hand
        second_split = False
        third_split = False
        fourth_split = False
        result_split = {}
        conclude_split = {}
        if insurance_take:
            bet_split = (player_deal.balance() - insurance_payment) / total_hand
        else:
            bet_split = player_deal.balance() / total_hand
        for _ in list(range(0, total_hand)):
            while True:
                if insurance_take != None:
                    print(game_log(player_status, player_wallet.balance(), player_deal.balance(), player_insurance), flush = True)
                else:
                    print(game_log(player_status, player_wallet.balance(), player_deal.balance()), flush = True)
                game_table(dealer_hand).facedown()
                if player_split == 4:
                    fourth_split = True
                    game_table(player_hand).faceup("Player", "1st")
                    game_table(second_hand).faceup("Player", "2nd")
                    game_table(third_hand).faceup("Player", "3rd")
                    player_value = game_table(fourth_hand).faceup("Player", "4th")
                elif player_split == 3:
                    third_split = True
                    game_table(player_hand).faceup("Player", "1st")
                    game_table(second_hand).faceup("Player", "2nd")
                    player_value = game_table(third_hand).faceup("Player", "3rd")
                    if fourth_split:
                        game_table(fourth_hand).faceup("Player", "4th")
                elif player_split == 2:
                    second_split = True
                    game_table(player_hand).faceup("Player", "1st")
                    player_value = game_table(second_hand).faceup("Player", "2nd")
                    if third_split:
                        game_table(third_hand).faceup("Player", "3rd")
                        if fourth_split:
                            game_table(fourth_hand).faceup("Player", "4th")
                else:
                    player_value = game_table(player_hand).faceup("Player", "1st")
                    game_table(second_hand).faceup("Player", "2nd")
                    if third_split:
                        game_table(third_hand).faceup("Player", "3rd")
                        if fourth_split:
                            game_table(fourth_hand).faceup("Player", "4th")
                if player_value > 21:
                    player_stand = False
                    result_split[player_split] = 0
                    refresh_screen()
                    break
                elif player_value == 21:
                    player_stand = True
                    break
                else:
                    player_status = "Playing"
                    if player_split == 4:
                        present_hand = "4th-hand"
                    elif player_split == 3:
                        present_hand = "3rd-hand"
                    elif player_split == 2:
                        present_hand = "2nd-hand"
                    else:
                        present_hand = "1st-hand"
                    player_option = input(f"\nDo you want to Hit(H) or Stand(S) for the {present_hand}? ")
                    if player_option.upper() == "H":
                        if player_split == 4:
                            fourth_hand.draw_card(blackjack_deck.draw())
                        elif player_split == 3:
                            third_hand.draw_card(blackjack_deck.draw())
                        elif player_split == 2:
                            second_hand.draw_card(blackjack_deck.draw())
                        else:
                            player_hand.draw_card(blackjack_deck.draw())
                        refresh_screen()
                        continue
                    elif player_option.upper() == "S":
                        player_stand = True
                        break
                    else:
                        player_status = "Wrong input!"
                        refresh_screen()
                        continue
            if player_stand:
                if (player_split == 4) and fourth_split:
                    player_status = "4th-hand stand!"
                elif (player_split == 3) and third_split:
                    player_status = "3rd-hand stand!"
                elif (player_split == 2) and second_split:
                    player_status = "2nd-hand stand!"
                else:
                    player_status = "Stand!"
                result_split[player_split] = player_value
                refresh_screen()
            if player_split == 4:
                third_hand.draw_card(blackjack_deck.draw())
            elif player_split == 3:
                second_hand.draw_card(blackjack_deck.draw())
            elif player_split == 2:
                player_hand.draw_card(blackjack_deck.draw())
            player_split -= 1
        if insurance_take != None:
            print(game_log(player_status, player_wallet.balance(), player_deal.balance(), player_insurance), flush = True)
        else:
            print(game_log(player_status, player_wallet.balance(), player_deal.balance()), flush = True)
        game_table(dealer_hand).faceup("Dealer")
        if total_hand == 2:
            game_table(player_hand).faceup("Player", "1st")
            game_table(second_hand).faceup("Player", "2nd")
        elif total_hand == 3:
            game_table(player_hand).faceup("Player", "1st")
            game_table(second_hand).faceup("Player", "2nd")
            game_table(third_hand).faceup("Player", "3rd")
        elif total_hand == 4:
            game_table(player_hand).faceup("Player", "1st")
            game_table(second_hand).faceup("Player", "2nd")
            game_table(third_hand).faceup("Player", "3rd")
            game_table(fourth_hand).faceup("Player", "4th")
        # Insurance results
        if insurance_take:
            if dealer_value == 21:
                player_insurance = "Win!"
                player_wallet.deposit(insurance_payment + game_calculator(insurance_payment).insurance_payout())
                player_deal.withdraw(insurance_payment)
            else:
                player_insurance = "Lose!"
                player_deal.withdraw(insurance_payment)
        # Split game results
        if all([True if hand_result == 0 else False for _, hand_result in result_split.items()]):
            player_status = "All-bust!"
            hand_number = 1
            for _ in list(range(0, len(result_split.items()))):
                conclude_split[hand_number] = "Bust!"
                hand_number += 1
            player_deal.withdraw(player_deal.balance())
        else:
            # Dealer turns
            while dealer_value < 17:
                dealer_hand.draw_card(blackjack_deck.draw())
                dealer_value = game_table(dealer_hand).faceup(hand_owner = "Dealer", print_output = False)
                if dealer_value < 17:
                    sleep(1.5)
                    refresh_screen()
                    if insurance_take != None:
                        print(game_log(player_status, player_wallet.balance(), player_deal.balance(), player_insurance), flush = True)
                    else:
                        print(game_log(player_status, player_wallet.balance(), player_deal.balance()), flush = True)
                    game_table(dealer_hand).faceup("Dealer")
                    if total_hand == 2:
                        game_table(player_hand).faceup("Player", "1st")
                        game_table(second_hand).faceup("Player", "2nd")
                    elif total_hand == 3:
                        game_table(player_hand).faceup("Player", "1st")
                        game_table(second_hand).faceup("Player", "2nd")
                        game_table(third_hand).faceup("Player", "3rd")
                    elif total_hand == 4:
                        game_table(player_hand).faceup("Player", "1st")
                        game_table(second_hand).faceup("Player", "2nd")
                        game_table(third_hand).faceup("Player", "3rd")
                        game_table(fourth_hand).faceup("Player", "4th")
            # Split game results
            for hand_number, hand_result in list(result_split.items())[::-1]:
                if hand_result == 0:
                    conclude_split[hand_number] = "Bust!"
                else:
                    if dealer_value == hand_result:
                        conclude_split[hand_number] = "Push!"
                        player_wallet.deposit(bet_split)
                    elif (dealer_value > 21) or (dealer_value < hand_result):
                        conclude_split[hand_number] = "Win!"
                        player_wallet.deposit(game_calculator(bet_split).win_payout())
                    else:
                        conclude_split[hand_number] = "Lose!"
                player_deal.withdraw(bet_split)
            player_status = "Split concluded!"
            sleep(1.5)
    # No split game
    else:
        onetime_offer = True
        player_surrender = False
        player_bust = False
        while True:
            if insurance_take != None:
                print(game_log(player_status, player_wallet.balance(), player_deal.balance(), player_insurance), flush = True)
            else:
                print(game_log(player_status, player_wallet.balance(), player_deal.balance()), flush = True)
            game_table(dealer_hand).facedown()
            player_value = game_table(player_hand).faceup("Player")
            if player_value > 21:
                player_bust = True
                refresh_screen()
                break
            elif player_value == 21:
                player_stand = True
                break
            else:
                player_status = "Playing"
                if onetime_offer:
                    onetime_offer = False
                    first_option = True
                    if insurance_take:
                        onetime_deal = player_deal.balance() - insurance_payment
                    else:
                        onetime_deal = player_deal.balance()
                    if onetime_deal <= player_wallet.balance():
                        player_option = input("\nDo you want to Hit(H) or Double(D) or Stand(S) or Surrender(X)? ")
                        if player_option.upper() == "D":
                            player_wallet.withdraw(onetime_deal)
                            player_deal.deposit(onetime_deal)
                            player_hand.draw_card(blackjack_deck.draw())
                            player_value = game_table(player_hand).faceup(hand_owner = "Player", print_output = False)
                            if player_value > 21:
                                continue
                            else:
                                player_stand = True
                                break
                    else:
                        player_option = input("\nDo you want to Hit(H) or Stand(S) or Surrender(X)? ")
                    if player_option.upper() == "X":
                        player_surrender = True
                        refresh_screen()
                        break
                else:
                    first_option = False
                    player_option = input("\nDo you want to Hit(H) or Stand(S)? ")
                if player_option.upper() == "H":
                    player_hand.draw_card(blackjack_deck.draw())
                    refresh_screen()
                    continue
                elif player_option.upper() == "S":
                    player_stand = True
                    break
                else:
                    if first_option:
                        onetime_offer = True
                    player_status = "Wrong input!"
                    refresh_screen()
                    continue
        if player_stand:
            player_status = "Stand!"
            refresh_screen()
        if insurance_take != None:
            print(game_log(player_status, player_wallet.balance(), player_deal.balance(), player_insurance), flush = True)
        else:
            print(game_log(player_status, player_wallet.balance(), player_deal.balance()), flush = True)
        game_table(dealer_hand).faceup("Dealer")
        game_table(player_hand).faceup("Player")
        # Insurance results
        if insurance_take:
            if dealer_value == 21:
                player_insurance = "Win!"
                player_wallet.deposit(insurance_payment + game_calculator(insurance_payment).insurance_payout())
                player_deal.withdraw(insurance_payment)
            else:
                player_insurance = "Lose!"
                player_deal.withdraw(insurance_payment)
        # No split game results
        if player_bust:
            player_status = "Bust!"
        elif player_surrender:
            player_status = "Surrender!"
            player_wallet.deposit(player_deal.balance() / 2)
        else:
            # Dealer turns
            while dealer_value < 17:
                dealer_hand.draw_card(blackjack_deck.draw())
                dealer_value = game_table(dealer_hand).faceup(hand_owner = "Dealer", print_output = False)
                if dealer_value < 17:
                    sleep(1.5)
                    refresh_screen()
                    if insurance_take != None:
                        print(game_log(player_status, player_wallet.balance(), player_deal.balance(), player_insurance), flush = True)
                    else:
                        print(game_log(player_status, player_wallet.balance(), player_deal.balance()), flush = True)
                    game_table(dealer_hand).faceup("Dealer")
                    game_table(player_hand).faceup("Player")
            # No split game results
            if dealer_value == player_value:
                player_status = "Push!"
                player_wallet.deposit(player_deal.balance())
            elif (dealer_value > 21) or (dealer_value < player_value):
                player_status = "Win!"
                player_wallet.deposit(game_calculator(player_deal.balance()).win_payout())
            else:
                player_status = "Lose!"
            sleep(1.5)
        player_deal.withdraw(player_deal.balance())
    # Game final results
    while True:
        if (player_wallet.balance() >= 1) or player_quit:
            refresh_screen()
            if insurance_take != None:
                print(game_log(player_status, player_wallet.balance(), player_deal.balance(), player_insurance), flush = True)
            else:
                print(game_log(player_status, player_wallet.balance(), player_deal.balance()), flush = True)
            game_table(dealer_hand).faceup("Dealer")
            if total_hand == 1:
                game_table(player_hand).faceup("Player")
            elif total_hand == 2:
                game_table(player_hand).faceup("Player", "1st", conclude_split[1])
                game_table(second_hand).faceup("Player", "2nd", conclude_split[2])
            elif total_hand == 3:
                game_table(player_hand).faceup("Player", "1st", conclude_split[1])
                game_table(second_hand).faceup("Player", "2nd", conclude_split[2])
                game_table(third_hand).faceup("Player", "3rd", conclude_split[3])
            elif total_hand == 4:
                game_table(player_hand).faceup("Player", "1st", conclude_split[1])
                game_table(second_hand).faceup("Player", "2nd", conclude_split[2])
                game_table(third_hand).faceup("Player", "3rd", conclude_split[3])
                game_table(fourth_hand).faceup("Player", "4th", conclude_split[4])
        if player_quit:
            if player_left:
                if player_wallet.balance() >= float(1000):
                    player_profit = player_wallet.balance() - float(1000)
                    print(f"\nYour profit: ${player_profit}", flush = True)
                elif player_wallet.balance() < float(1000):
                    player_loss = float(1000) - player_wallet.balance()
                    print(f"\nYour loss: ${player_loss}", flush = True)
                print("I\'ll see you again :)", flush = True)
            else:
                print("\nInsufficient money to continue playing the game. Goodbye!", flush = True)
            break
        elif player_wallet.balance() >= 1:
            play_again = input("\nWould you like to continue playing the game (Y or N)? ")
            if play_again.upper() == "Y":
                refresh_screen()
                break
            elif play_again.upper() == "N":
                player_quit = True
                player_left = True
                player_status = "The End"
                continue
            else:
                player_status = "Wrong input!"
                refresh_screen()
                continue
        else:
            player_quit = True
            player_left = False
            player_status = "Game Over"
            continue
    if player_quit:
        sys.exit()
    else:
        start_game(player_wallet.balance())

def start_game(player_money = 1000):
    refresh_screen()
    introduction = True
    player_cancel = False
    player_wallet = game_safe(player_money)
    player_deal = game_safe(0)
    while True:
        if introduction:
            introduction = False
            player_status = "Bet or Enter nothing to quit"
            print("    PyBj (Python Blackjack)", flush = True)
            print("   ver 1.0 build 220405.0001", flush=True)
            print("       by Ade Destrianto\n", flush=True)
            print("*==" * 10 + "*", flush = True)
            print(" *   Blackjack pays 3 to 2   *", flush = True)
            print("  *  Insurance pays 2 to 1  * ", flush = True)
            print(" *  A $1000 & six-deck game  *", flush = True)
            print("*==" * 10 + "*\n", flush = True)
            if player_cancel:
                print("Hesitating? Maybe next time? ;)", flush = True)
                sys.exit()
        print(game_log(player_status, player_wallet.balance(), player_deal.balance()), flush = True)
        print("\nAvailable chips", flush = True)
        print("=" * 15, flush = True)
        for chip_option in game_chip().value().keys():
            print(f"[{chip_option}]", game_chip().color(chip_option), flush = True)
        player_chip = input("\nWhich chip do you want to place as a bet (1 - 6)? ")
        if player_chip.isnumeric():
            player_chip = int(player_chip)
            if player_chip in game_chip().value().keys():
                player_chip = float(game_chip().value()[player_chip])
                if player_chip > player_wallet.balance():
                    player_status = "Your bet exceeded your money!"
                    refresh_screen()
                    continue
                else:
                    player_status = "Raise the bet or Enter nothing to deal"
                    player_wallet.withdraw(player_chip)
                    player_deal.deposit(player_chip)
                    if player_wallet.balance() > 0:
                        refresh_screen()
                        continue
                    else:
                        player_status = "Playing"
                        refresh_screen()
                        break
            else:
                player_status = "The chip is not available!"
                refresh_screen()
                continue
        elif bool(player_chip) == False:
            if player_deal.balance() > 0:
                player_status = "Playing"
                refresh_screen()
                break
            else:
                player_cancel = True
                introduction = True
                refresh_screen()
                continue
        else:
            player_status = "Wrong input!"
            refresh_screen()
            continue
    game_play(player_status, player_wallet, player_deal)