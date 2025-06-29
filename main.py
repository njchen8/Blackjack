import algo
import random

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

def deal(deck):
    """Deal a card from the deck."""
    available_cards = [card for card, count in deck.items() if count > 0]
    if not available_cards:
        return None
    
    card = random.choice(available_cards)
    deck[card] -= 1
    return card
    
def main():
    game_count = 0
    player_wins = 0
    dealer_wins = 0
    ties = 0
    
    while sum(deck.values()) >= 4:  # Need at least 4 cards for a game
        game_count += 1
        print(f"\n=== GAME {game_count} ===")
        print(f"Cards remaining in deck: {sum(deck.values())}")
        
        # Deal initial cards
        player_hand = [deal(deck), deal(deck)]
        dealer_hand = [deal(deck)]  # Dealer starts with only 1 card
        
        if None in player_hand or dealer_hand[0] is None:
            print("Not enough cards to continue!")
            break
            
        print("Player's hand:", player_hand, f"(Total: {sum(player_hand)})")
        print("Dealer's hand:", dealer_hand[0], "and a hidden card")
        
        # Player's turn - keep hitting until they stand or bust
        player_busted = False
        while True:
            player_total = sum(player_hand)
            if player_total > 21:
                print("Player busts! Dealer wins.")
                dealer_wins += 1
                player_busted = True
                break
                
            move = algo.next_move(deck, player_hand, dealer_hand)
            print("Recommended move:", move)
            print("Current odds of winning:", f"{algo.odds_i_win(deck, player_hand, dealer_hand):.4f}")
            print("Current odds of dealer winning:", f"{algo.odds_dealer_wins(deck, player_hand, dealer_hand):.4f}")
            
            player_move = input("Enter your move (hit/stand): ").strip().lower()
            while player_move not in ["hit", "stand"]:
                player_move = input("Invalid move. Enter 'hit' or 'stand': ").strip().lower()
            
            if player_move == "hit":
                new_card = deal(deck)
                if new_card is None:
                    print("No more cards in deck!")
                    break
                player_hand.append(new_card)
                print("Player's hand after hit:", player_hand, f"(Total: {sum(player_hand)})")
            elif player_move == "stand":
                print("Player stands with hand:", player_hand, f"(Total: {sum(player_hand)})")
                break
        
        # Only proceed to dealer's turn if player didn't bust
        if not player_busted:
            # Dealer's turn - only happens after player stands
            print("\nDealer's turn...")
            # Deal the dealer's second card now
            second_card = deal(deck)
            if second_card is None:
                print("Not enough cards for dealer!")
                break
            dealer_hand.append(second_card)
            print("Dealer reveals hidden card. Dealer's hand:", dealer_hand, f"(Total: {sum(dealer_hand)})")
            
            while sum(dealer_hand) < 17:
                new_card = deal(deck)
                if new_card is None:
                    print("No more cards in deck!")
                    break
                dealer_hand.append(new_card)
                print(f"Dealer hits and gets {new_card}. Dealer's hand:", dealer_hand, f"(Total: {sum(dealer_hand)})")
            
            print("Final dealer hand:", dealer_hand, f"(Total: {sum(dealer_hand)})")
            
            # Determine winner
            player_total = sum(player_hand)
            dealer_total = sum(dealer_hand)
            
            if dealer_total > 21:
                print("Dealer busts! Player wins.")
                player_wins += 1
            elif dealer_total > player_total:
                print("Dealer wins.")
                dealer_wins += 1
            elif dealer_total < player_total:
                print("Player wins.")
                player_wins += 1
            else:
                print("It's a tie!")
                ties += 1
        
        print(f"\nGame {game_count} complete!")
    
    # Final statistics
    print(f"\n=== FINAL STATISTICS ===")
    print(f"Total games played: {game_count}")
    print(f"Player wins: {player_wins} ({player_wins/game_count*100:.1f}%)")
    print(f"Dealer wins: {dealer_wins} ({dealer_wins/game_count*100:.1f}%)")
    print(f"Ties: {ties} ({ties/game_count*100:.1f}%)")
    print(f"Cards remaining: {sum(deck.values())}")

if __name__ == "__main__":
    main()