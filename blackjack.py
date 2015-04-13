# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.hand = []

    def __str__(self):
        # return a string representation of a hand
        a = "hand contains: "
        b = ""
        for i in range(len(self.hand)):
            b += str(self.hand[i]) + " "
        return a + b

    def add_card(self, card):
        # add a card object to a hand
        self.hand.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value = 0
        for card in self.hand:
            value += VALUES[card.rank]
        for card in self.hand:
            if card.rank == 'A':
                if value <= 11:
                    value += 10
                    break
        return value
   
    def draw(self, canvas, pos):
        for card in self.hand:
            card.draw(canvas, pos)
            pos[0] += 100
 
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit,rank))

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck
        return self.deck.pop()
    
    def __str__(self):
        # return a string representing the deck
        a = "Deck contains: "
        b = ""
        for card in range(len(self.deck)):
            b += str(self.deck[card]) + " "
        return a + b



#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hand, com_hand, score

    # your code goes here
    if not in_play:
        deck = Deck()
        Deck.shuffle(deck)
        player_hand = Hand()
        com_hand = Hand()
        player_hand.add_card(deck.deal_card())
        com_hand.add_card(deck.deal_card())
        player_hand.add_card(deck.deal_card())
        com_hand.add_card(deck.deal_card())
        print "Player " + str(player_hand)
        print "Com " + str(com_hand)
        in_play = True
        outcome = "Hit or stand?"
    else:
        outcome = "Bad move homie...New deal?"
        score -= 1
        in_play = False

def hit():
    # if the hand is in play, hit the player
    global in_play, score, outcome
    if in_play:
        player_hand.add_card(deck.deal_card())
        print "Player " + str(player_hand)
        if player_hand.get_value() >= 22:
            outcome = "You bust homie!  New deal?"
            score -=1
            in_play = False
        else:
            outcome = "Hit or stand?"
        
def stand():
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    global in_play, score, outcome
    if in_play:
        for i in range(52):
            if com_hand.get_value() >= 17:
                in_play = False
                break
            else:
                com_hand.add_card(deck.deal_card())
            print "Com " + str(com_hand)
    # assign a message to outcome, update in_play and score
        if com_hand.get_value() > 21:
            outcome = "Com busted you win homie!! New deal?"
            score += 1
        elif player_hand.get_value() <= com_hand.get_value():
            outcome = "You lose homie :(  New deal?"
            score -= 1
        else:
            outcome = "You Got Dis!!  New deal?"
            score += 1

        
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("BLACKJACK", [180, 50], 50, "Black")
    canvas.draw_text("Player Cards", [100, 100], 30, "Black")
    player_hand.draw(canvas, [100,150])
    canvas.draw_text("Com Cards", [100, 300], 30, "Black")
    com_hand.draw(canvas, [100, 350])
    canvas.draw_text(outcome, [100, 500], 30, "Yellow")
    canvas.draw_text("Score: " + str(score), [450, 100], 30, "Purple")
    
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [136, 398], CARD_SIZE)


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
