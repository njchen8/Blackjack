import numpy as np
import math 
deck = {    1: 4,  # Aces
            2: 4,  # Twos
            3: 4,  # Threes
            4: 4,  # Fours
            5: 4,  # Fives
            6: 4,  # Sixes
            7: 4,  # Sevens
            8: 4,  # Eights
            9: 4,  # Nines
            10: 16,  # Tens, Jacks, Queens, Kings
        }
cards_left = sum(deck.values())
def calculate_probability(deck, card):
    cards_left = sum(deck.values())
    if cards_left == 0:
        return 0
    return deck.get(card, 0) / cards_left

def odds_dealer_wins(deck, player_total, dealer_hand):
    ans = 0
    for key in deck:
        prob = calculate_probability(deck, key)
        if prob > 0:
            dealer_total = sum(dealer_hand) + key
        if dealer_total < 17:
            update_deck(deck, key)
            ans += odds_dealer_wins(deck, player_total, dealer_total)
        if dealer_total > player_total and dealer_total <= 21:     
            ans += prob
        if dealer_hand > 21:
            continue
    return ans

def odds_i_win(deck, player_hand, dealer_hand):
    ans = 1 - odds_dealer_wins(deck, sum(player_hand), dealer_hand) - calculate_probability(deck, 21 - sum(player_hand))
    return ans

def update_deck(deck, card):
    if card in deck:
        deck[card] -= 1
        cards_left -= 1
    else:
        raise ValueError("Card not in deck")
    
def next_move(deck, player_hand, dealer_hand):
    current_odds = odds_i_win(deck, player_hand, dealer_hand)
    hit_odds = 0
    for key in deck:
        prob = calculate_probability(deck, key)
        if prob > 0:
            new_player_hand = player_hand + [key]
            new_odds = odds_i_win(deck, new_player_hand, dealer_hand)
            hit_odds += prob * new_odds
    if hit_odds > current_odds:
        return "hit"
    return "stand"

        