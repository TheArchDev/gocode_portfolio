'''

BlackJack Game

User Stories:

1) User can play the blackjack game in terminal against the dealer
2) Dealer automatically plays his hand with a fixed algorithm (If it's 16 or below they hit, if it's above 16, they stay)
3) User can play the blackjack game repeatedly
4) User can choose to hit or stay
5) User can see what cards they have been dealt
6) User can only see one dealer card, not the bottom card

Tips:
1) Aces can count as an eleven or a one - but it only counts as a one if your score is over 21
2) Research random.shuffle()
3) You are not allowed to code until you design your program!
4) Optional: Research __radd__ - it is a built-in method in Python

Extension:
1) Multiple users can play blackjack game in terminal in a turn-based game
2) Consider using the stack data structure
3) User can bet dollar amounts in the blackjack game


'''

import random

class Card(object):
	def __init__(self,suit,pip,points):
		self.suit = suit
		self.pip = pip
		self.points = points
		self.title = str(pip) + " of " + str(suit)

class  Deck(object):
	def __init__(self):
		self.suit_types = ["Spades", "Hearts", "Clubs", "Diamonds"]
		self.pip_types = [(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),("Jack",10),("Queen",10),("King",10), ("Ace",11)]
		self.all_cards_in_deck = [Card(suit,pip[0],pip[1]) for suit in self.suit_types for pip in self.pip_types]
		#Alternative using a single dictionary, rather than an array of tuples. But in that case, don't necessarily get a deck in original hierarchy, without being shuffled.
		#self.pip_types = {2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10, "Jack":10, "Queen": 10, "King": 10, "Ace":11}
		#self.all_cards_in_deck = [Card(suit,pip,point) for suit in self.suit_types for pip,point in self.pip_types.items()]

	def show_deck(self):
		for card in self.all_cards_in_deck:
			print card.title
		print "There are " + str(len(self.all_cards_in_deck)) + " cards in the deck."

	def shuffle_deck(self):
		random.shuffle(self.all_cards_in_deck)
		print "Deck has been shuffled."

	def burn_card(self):
		pass


class Hand(object):
	def __init__(self):
		self.cards_in_hand = []
		self.points_total = 0
		self.deck = None
		self.name = None
		self.bust = False

	def show_hand(self):
		#self.recalculate_points()
		print self.name + " has the following hand:"
		for card in self.cards_in_hand:
			print card.title
		print "...which totals " + str(self.points_total) + " points"
		print

	def recalculate_points(self):
		self.points_total = sum([card.points for card in self.cards_in_hand])

	def draw_card(self, deck):
		self.cards_in_hand.append(deck.all_cards_in_deck.pop())
		self.recalculate_points()
		#could add a line that will print what card was drawn in the case of a human player (though do have show_hand function). Related to that, am I meant to see what the dealer draws?

	def check_for_ace(self):
		#edge case of if you get dealt two aces straight away. My approach only converts one of them from 11 to 1 at a time.
		for card in self.cards_in_hand:
			if card.pip == "Ace" and card.points == 11:
				card.points = 1
				print "Ace value has been changed from 11 to 1."
				self.recalculate_points()
				return True

class Human(Hand):
	def __init__(self, name):
		super(Human,self). __init__()
		self.name = name
		#include self.bust = True or False

	def play_turn(self):
		self.show_hand()
		while self.points_total <= 21:
			user_choice = raw_input("Would you like to HIT or STAY? ").upper().strip()
			if user_choice == "HIT":
				print self.name + " selected HIT"
				print
				self.draw_card(self.deck)
				self.show_hand()
				if self.points_total > 21:
					if self.check_for_ace() == True:
						self.show_hand()
						continue
					print self.name + " is bust!"
					self.bust = True
					print
					raw_input()
					return
			elif user_choice == "STAY":
				print self.name + " selected STAY\n"
				raw_input()
				return
			else:
				print "Invalid input. Please enter 'HIT' or 'STAY'"

class Dealer(Hand):
	def __init__(self):
		super(Dealer, self). __init__()
		self.name = "Devilish Dealer"

	def play_turn(self):
		while self.points_total <= 16:
			print self.name +  " selected HIT"
			#Am I meant to be seeing these newly-drawn cards? Suppose it doesn't make a difference, as all the humans have already played and I'll see them at the end.
			self.draw_card(self.deck)
			print
			raw_input()
			if self.points_total > 21:
				if self.check_for_ace() == True:
					continue
				self.show_hand()
				self.bust = True
				print self.name + " is bust!\n"
				raw_input()
				return
		print "Dealer selected STAY"
		raw_input()
		return

class Game(object):
	def __init__(self):
		self.deck = Deck()
		self.dealer = Dealer()
		self.players_in_game = []
		print "Please add human players (no need to add a dealer)."
		raw_input()

	def add_player(self, new_player):
		self.players_in_game.append(new_player)
		new_player.deck = self.deck
		print new_player.name + " was successfully added to the game."
		raw_input()

	def show_all_human_player_hands(self):
		#worth including a recalculate_all_player_points() ?? Probably an unnecessary safety net
		for player_hand in self.players_in_game:
			if player_hand != self.dealer:
				player_hand.show_hand()

	def show_all_player_hands(self):
		#worth including a recalculate_all_player_points() ??
		for player_hand in self.players_in_game:
			player_hand.show_hand()


	def recalculate_all_player_points(self):
		for player_hand in self.players_in_game:
			player_hand.recalculate_points()

	def reset_all_bust_attributes(self):
		for hand in self.players_in_game:
			hand.bust = False

	def gather_cards_back(self):
		self.deck.all_cards_in_deck += [hand.cards_in_hand.pop() for hand in self.players_in_game for x in range(0,len(hand.cards_in_hand))]

		self.recalculate_all_player_points()
		self.reset_all_bust_attributes()

		print "The deck has been gathered back in and all player hands reset."


	def all_draw_a_card(self):
		for player in self.players_in_game:
			player.draw_card(self.deck)
		print "One card was dealt to each player.\n"

	def initial_game_deal(self):
		self.all_draw_a_card()
		self.all_draw_a_card()

		self.show_all_human_player_hands()
		print self.dealer.name + "'s second card is: " + self.dealer.cards_in_hand[1].title
		raw_input()

	#a function to check if all human players have gone bust? Could use in game_turns()...

	def game_turns(self):
		all_busted = True
		for player in self.players_in_game:
			print "\t" + player.name + "'s turn to play!\n==>\n"
			if player == self.dealer and all_busted == True:
				print "Everyone is bust! No need for the dealer to play his turn."
				continue
			player.play_turn()
			if player.bust == True:
				continue
			all_busted = False

		print "\t RESULT TIME\n==>"

		if all_busted == True:
			print "All human players loose against the dealer.\n"
			return

		self.show_all_player_hands()
		raw_input()

		for player in self.players_in_game[:len(self.players_in_game)-1]:
			if player.bust == False and self.dealer.bust == True:
				print player.name + " beats the " + self.dealer.name + ", who went bust!"
			elif player.bust == False and self.dealer.bust == False:
				if player.points_total > self.dealer.points_total:
					print player.name + " beats the " + self.dealer.name
				elif player.points_total == self.dealer.points_total:
					print player.name + " draws with the " + self.dealer.name
				elif player.points_total < self.dealer.points_total:
					print player.name + " loses to the " + self.dealer.name
			elif player.bust == True and self.dealer.bust == True:
				print player.name + " and the " + self.dealer.name + " both went bust!"
			elif player.bust == True and self.dealer.bust == False:
				print player.name + ", who went bust, loses to the " + self.dealer.name


	def calculate_winner(self):
		pass

	def play_game(self):
		print "A deck has been gathered."
		self.add_player(self.dealer)
		while True:
			print "LET'S PLAY BLACKJACK!\n"
			self.deck.shuffle_deck()
			print

			self.initial_game_deal()
			self.game_turns()

			self.gather_cards_back()
			play_again = raw_input("Enter YES if you'd like to play again? ").upper().strip()
			if play_again == "YES":
				print
				continue
				#could also use continue in this scenario
			print "Thanks for playing!\n"
			break


first_player = Human("Alex")
second_player = Human("Tony")
third_player = Human("Leo")

test_game = Game()
test_game.add_player(first_player)
test_game.add_player(second_player)
test_game.add_player(third_player)
test_game.play_game()












