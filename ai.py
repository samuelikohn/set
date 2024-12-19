from itertools import combinations
from PyQt6.QtCore import QTimer
from random import shuffle
    

class AI:

    def click_card(self):
        self.board.card_clicked(self.set[self.card_index], "ai")
        self.card_index += 1
        if self.card_index == len(self.set):
            self.found_timer.stop()
            self.in_selection = False

    def destroy(self):
        self.timer.deleteLater()
        self.found_timer.deleteLater()
        self.board.ai = None

    # When AI finds a SET
    def found_set(self):
        self.in_selection = True
        self.stop()
        self.board.call_set_btn.called = True # Prevent player from activating Call Set button
        self.board.call_set_btn.setText("Too Slow!")
        self.card_index = 0
        self.found_timer.start(500)

    def pause(self):
        if self.in_selection:
            self.found_timer.stop()
        else:
            self.remaining_time = self.timer.remainingTime()
            self.timer.stop()

    def resume(self):
        if self.in_selection:
            self.found_timer.start(300)
        else:
            self.timer.start(self.remaining_time)
    
    # Each increment of self.steps represents a decision a human would make following this algorithm
    def search(self, board, traits):

        # Step 1: if there is any trait with less than max variations, search each variation of that trait
        shuffle(traits)
        for trait in traits:
            self.steps += 1

            # Count number of variations of current trait on the board
            variations = set()
            shuffle(board)
            for card in board:

                self.steps += 3

                variations.add(getattr(card, trait))
                if len(variations) == self.board.num_variations:
                    break

            # Call search if less than max
            if len(variations) < self.board.num_variations:
                self.steps += 1

                for variation in variations:
                    self.steps += 3 + 2 * len(board)

                    next_board = [card for card in board if getattr(card, trait) == variation] # Filter board to only include cards with current variation

                    # If exactly num_variations cards, check if they form a SET
                    if len(next_board) == self.board.num_variations and self.board.is_set(next_board):
                        self.steps += len(traits) * len(next_board)

                        self.set = next_board
                        
                        return True

                    # If more than num_variations cards, search
                    elif len(next_board) > self.board.num_variations:
                        next_traits = traits.copy()
                        next_traits.remove(trait)
                        self.steps += 1

                        return self.search(next_board, next_traits)
                    
                return False

        # Step 2: search each variation of each trait
        shuffle(traits)
        for trait in traits:
            self.steps += 1
            
            variations = self.board.all_properties[trait]
            shuffle(variations)
            for variation in variations:
                self.steps += 3 + 2 * len(board)

                next_board = [card for card in board if getattr(card, trait) == variation] # Filter board to only include cards with current variation

                # If exactly num_variations cards, check if they form a SET
                if len(next_board) == self.board.num_variations and self.board.is_set(next_board):
                    self.steps += len(traits) * len(next_board)

                    self.set = next_board

                    return True

                # If more than num_variations cards, search
                elif len(next_board) > self.board.num_variations:
                    next_traits = traits.copy()
                    next_traits.remove(trait)
                    self.steps += 1

                    if self.search(next_board, next_traits):
                        return True

        # Step 3: brute force search
        for cards in combinations(board, 2):
            self.steps += 1
            
            # Check if any 2 cards have different traits
            if all(getattr(cards[0], trait) != getattr(cards[1], trait) for trait in traits):
                self.steps += len(traits)

                shuffle(board)
                for card3 in board:

                    # Check every card after the 2nd if its traits are all different
                    if card3.card_pos > cards[1].card_pos and all(getattr(card3, trait) != getattr(cards[0], trait) and getattr(card3, trait) != getattr(cards[1], trait) for trait in traits):
                        self.steps += 2 + 2 * len(traits)
                        
                        # If 3 cards per SET, then SET found
                        if self.board.num_variations == 3:

                            self.set = [cards[0], cards[1], card3]

                            return True
                        else:

                            # Check every card after the 3rd if its traits are all different
                            for card4 in board:
                                self.steps += 1

                                if card4.card_pos > card3.card_pos and all(getattr(card4, trait) != getattr(cards[0], trait) and getattr(card4, trait) != getattr(cards[1], trait) and getattr(card4, trait) != getattr(card3, trait) for trait in traits):
                                    self.steps += 2 + 2 * len(traits)

                                    # If 4 cards per SET, then SET found
                                    if self.board.num_variations == 4:

                                        self.set = [cards[0], cards[1], card3, card4]

                                        return True
                                    else:

                                        # Check every card after the 4th if its traits are all different
                                        for card5 in board:
                                            self.steps += 1
                                            
                                            if card5.card_pos > card4.card_pos and all(getattr(card5, trait) != getattr(cards[0], trait) and getattr(card5, trait) != getattr(cards[1], trait) and getattr(card5, trait) != getattr(card3, trait) and getattr(card5, trait) != getattr(card4, trait) for trait in traits):
                                                self.steps += 1 + 2 * len(traits)

                                                self.set = [cards[0], cards[1], card3, card4, card5]
                                                
                                                return True

        return False
    
    def start(self):
        self.steps = 0
        if self.search(self.board.current_board, self.board.all_traits):
            self.timer.start(int(self.steps * self.ms_per_step * self.difficulty_multiplier))

    def stop(self):
        self.timer.stop()

    def __init__(self, board, difficulty_multiplier):
        self.board = board
        self.difficulty_multiplier = difficulty_multiplier
        self.steps = 0
        self.timer = QTimer(parent = self.board.main.central_widget)
        self.timer.timeout.connect(self.found_set)
        self.remaining_time = 0
        self.ms_per_step = 15 # Subject to change. Need to vary with traits/variation combos?

        # For displaying AI found SETs
        self.in_selection = False
        self.set = None
        self.card_index = 0
        self.found_timer = QTimer(parent = self.board.main.central_widget)
        self.found_timer.timeout.connect(self.click_card)