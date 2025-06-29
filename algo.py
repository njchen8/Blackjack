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

def odds_dealer_wins(deck, player_hand, dealer_hand):
    player_total = sum(player_hand)
    dealer_total = sum(dealer_hand)
    
    # Base cases - dealer's turn is complete
    if dealer_total >= 17:
        if dealer_total > 21:
            return 0  # Dealer busts, player wins
        elif dealer_total > player_total:
            return 1  # Dealer wins
        else:
            return 0  # Dealer loses or ties
    
    # Dealer must hit (total < 17)
    ans = 0
    for card in deck:
        prob = calculate_probability(deck, card)
        if prob > 0:
            new_dealer_hand = dealer_hand + [card]
            deck_copy = deck.copy()
            update_deck(deck_copy, card)
            ans += prob * odds_dealer_wins(deck_copy, player_hand, new_dealer_hand)
    
    return ans

def odds_i_win(deck, player_hand, dealer_hand):
    player_total = sum(player_hand)
    ans = 1 - odds_dealer_wins(deck, player_hand, dealer_hand) - calculate_probability(deck, 21 - player_total)
    return ans

def update_deck(deck, card):
    if card in deck:
        deck[card] -= 1
    else:
        raise ValueError("Card not in deck")
    
def next_move(deck, player_hand, dealer_hand):
    current_odds = odds_i_win(deck, player_hand, dealer_hand)
    hit_odds = 0
    
    for key in deck:
        prob = calculate_probability(deck, key)
        if prob > 0:
            new_player_hand = player_hand + [key]
            # Check if player busts
            if sum(new_player_hand) > 21:
                continue  # Skip this scenario as player loses
            deck_copy = deck.copy()
            update_deck(deck_copy, key)
            new_odds = odds_i_win(deck_copy, new_player_hand, dealer_hand)
            hit_odds += prob * new_odds
    
    # Print the probabilities
    print(f"Standing odds: {current_odds:.4f} ({current_odds*100:.2f}%)")
    print(f"Hitting odds: {hit_odds:.4f} ({hit_odds*100:.2f}%)")
    
    if hit_odds > current_odds:
        return "hit"
    return "stand"

