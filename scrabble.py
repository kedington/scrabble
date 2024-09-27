import random

LETTER_DISTRIBUTION = {
    'a': 9, 'b': 2, 'c': 2, 'd': 4, 'e': 12, 'f': 2, 'g': 3, 'h': 2, 'i': 9, 'j': 1, 'k': 1, 'l': 4, 'm': 2,
    'n': 6, 'o': 8, 'p': 2, 'q': 1, 'r': 6, 's': 4, 't': 6, 'u': 4, 'v': 2, 'w': 2, 'x': 1, 'y': 2, 'z': 1, ' ': 2
}

class Scrabble:
	def __init__(self):
		self.bag = [letter for letter, count in LETTER_DISTRIBUTION.items() for _ in range(count)]
		self.num_of_tiles = 100
	
	def get_tile(self):
		choice_index = random.randint(0, self.num_of_tiles-1)
		choice = self.bag[choice_index]	
		
		# Swap & Pop for efficent removal
		self.bag[choice_index] = self.bag[self.num_of_tiles-1]
		self.bag.pop()
		self.num_of_tiles -= 1
		
		return choice
	
	def get_starting_tiles(self):
		return [self.get_tile() for _ in range(7)]


class Dictionary:
	def __init__(self):
		self.dictionary = {letter: LetterNode(letter) for letter in LETTER_DISTRIBUTION if letter != ' '}
		words = []
		with open("nwl2020.txt", "r", encoding='utf-8', errors='ignore') as infile:
			for word in infile:
				words.append(word.split(" ")[0].lower())
		for word in words:
			letter_node = self.dictionary[word[0]]
			for letter in word[1:]:
				if letter not in letter_node.next_letters:
					letter_node.next_letters[letter] = LetterNode(letter)
				letter_node = letter_node.next_letters[letter]		
			letter_node.set_is_end_of_word()

	def is_word(self, word):
		letter_node = self.dictionary[word[0]]
		for letter in word[1:]:
			if letter not in letter_node.next_letters:
				return False
			letter_node = letter_node.next_letters[letter]		
		return letter_node.is_end_of_word

	def get_all_words(self,letters):
		all_words = []
		def recursive_helper(cur_letters, letter_node, path, words):
			if letter_node.is_end_of_word:
				words.append(path)
			for index in range(len(cur_letters)):
				letter = cur_letters[index]
				print(path + letter)
				if letter in letter_node.next_letters:
					recursive_helper(cur_letters[0:index] + cur_letters[index+1:], letter_node.next_letters[letter], path + letter, words)
		
		for index in range(len(letters)):
			recursive_helper(letters[0:index] + letters[index+1:], self.dictionary[letters[index]], letters[index], all_words)
				
				
		return all_words	

class LetterNode:
	def __init__(self, letter):
		self.letter = letter
		self.is_end_of_word = False
		self.next_letters = dict()
	
	def set_is_end_of_word(self):
		self.is_end_of_word = True
	
