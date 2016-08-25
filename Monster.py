import random
import Weapon
from Shared import *
from Names import name_generator, NAME_TYPES


def get_random_enemy(enemies_in_area, level_min,
							level_max, difficulty_min, difficulty_max,
							names_possible = None):
	""" Generates a random enemy with attributes from the given possibilities. """
	chosen_enemy = random.choice(enemies_in_area)
	if(names_possible is None):
		chosen_name = name_generator("fantasy")
	else:
		chosen_name = random.choice(names_possible)
	chosen_level = random.choice(range(level_min, level_max + 1))
	chosen_difficulty = random.choice(range(difficulty_min, difficulty_max + 1))
	return TYPES[chosen_enemy](chosen_name, chosen_level, chosen_difficulty)

class Monster(Character):
	""" Monsters representing Characters for the Players to kill. """
	difficulty_level = ("easy", "normal", "exceptional")

	def __init__(self, name, level = 1, difficulty = 1):
		""" Initializes a monster with given attributes."""
		self.name = name
		self.difficulty = difficulty
		self.level = level
		self.alive = True
		self.equipped_weapon = None
		self.experience = 0

	def deal_damage(self, damage):
		""" 
		Deals damage to the monster.
		Chastises user if the monter is dead.
		"""
		return super(Monster, self).deal_damage(damage, "attacking the dead creature has no effect")

	def level_up(self):
		""" Levels up the Monster"""
		super(Monster, self).level_up(False)

	def give_exp(self, amount):
		""" gives experience to the Monster, leveling up as necessary. """
		super(Monster, self).give_exp(amount, False)

	def __repr__(self):
		""" returns a representation of how to recreate the Monster"""
		return (self.class_name + "(" + self.name + ", " + 
						self.level + ", " + self.difficulty + ")")

	def __str__(self):
		""" returns a user friendly description of the monster """
		return self.name + " the " + self.class_name.lower()

	def display_inventory(self):
		""" Displays what the monster owns """
		super(Monster, self).display_inventory(False)

	def equip_item(self):
		""" equips item to monster """
		super(Monster, self).equip_item()

class Goblin(Monster):
	class_name = "goblin"
	desc = "\ta fairly weak mischievous, ugly, dwarflike creature"
	aptitude = ("\tincapable of using magic, this type of monster"
				+" also renders magic near useless against themselves")
	level_modifier = { 	# modifiers applied on level
		"health"		: 1.04,
		"attack"		: 1.05,
		"endurance"		: 1.02,
		"vitality"		: 1.08,
		"mana"			: 1,
		"movement speed": 1.04,
		"intellect"		: 1
	}

	def __init__(self, name, level = 1, difficulty = 1):
		""" Creates a goblin """
		super(Goblin, self).__init__(name, level, difficulty)
		self.modifiers = {		# modifiers for equipment
			"melee"				: .8,
			"melee defense"		: .75,
			"ranged"			: .8,
			"ranged defense"	: .75,
			"magic"				: 0,
			"defense"			: 1,
			"magic defense"		: 1.5,
			"fire resistance"	: .75,
			"ice resistance"	: .75,
			"speed"				: 1.2
		}

		self.statistics_base = {
			"health"		: 65 +  (15 * difficulty),
			"attack"		: 30 +  (10 * difficulty),
			"endurance"		: 80 +  (20 * difficulty),
			"vitality"		: 60 +  (8 * difficulty),
			"mana"			: 0,
			"movement speed": 90 +  (15 * difficulty),
			"intellect"		: 0
		}

		self.statistics = dict()
		for key in self.statistics_base:
			self.statistics_base[key] = (self.statistics_base[key]
									* (self.level_modifier[key] ** level))
		self.current_health = self.statistics_base["health"]
		self.current_mana = self.statistics_base["mana"]

		self.inventory = list()
		sword = Weapon.LongSword(1, 2, True)
		self.inventory.append(sword)
		self.equipped_weapon = sword
		self.drops = {
			"experience" 	: 45 * level,
			"gold"			: 25 * level,
			"items"			: self.inventory
		}

class Dragon(Monster):
	class_name = "dragon"
	desc = "\ta large conglomeration of a snake and a serpent"
	aptitude = ("\tgreatly resitant to fire")
	level_modifier = { 	# modifiers applied on level
		"health"		: 1.04,
		"attack"		: 1.1,
		"endurance"		: 1.02,
		"vitality"		: 1.08,
		"mana"			: 1,
		"movement speed": 1.04,
		"intellect"		: 1
	}

	def __init__(self, name, level = 1, difficulty = 1):
		""" creates a dragon """
		super(Dragon, self).__init__(name, level, difficulty)
		self.modifiers = {		# modifiers for equipment
			"melee"				: 1.2,
			"melee defense"		: 1.1,
			"ranged"			: 1.2,
			"ranged defense"	: 1,
			"magic"				: 1,
			"defense"			: 1,
			"magic defense"		: 1,
			"fire resistance"	: 2,
			"ice resistance"	: 2,
			"speed"				: 1.5
		}

		self.statistics_base = {
			"health"		: 120 +  (25 * difficulty),
			"attack"		: 125 +  (15 * difficulty),
			"endurance"		: 100 +  (20 * difficulty),
			"vitality"		: 80  +  (8 * difficulty),
			"mana"			: 100 +  (4 * difficulty),
			"movement speed": 135 +  (20 * difficulty),
			"intellect"		: 100 +  (5 * difficulty)
		}

		for key in self.statistics_base:
			self.statistics_base[key] = (self.statistics_base[key]
									* (self.level_modifier[key] ** level))
		self.current_health = self.statistics_base["health"]
		self.current_mana = self.statistics_base["mana"]

		self.inventory = list()
		self.inventory.append(Weapon.FireAndIceCrossBows(2,10,True))

		self.drops = {
			"experience" 	: 100 * level,
			"gold"			: 90 * level,
			"items"			: self.inventory
		}

class Eagle(Monster):
	class_name = "giant eagle"
	desc = "\ta giant american eagle"
	aptitude = ("\tparticularly fast and aggressive")
	level_modifier = { 	# modifiers applied on level
		"health"		: 1.06,
		"attack"		: 1.1,
		"endurance"		: 1.02,
		"vitality"		: 1.08,
		"mana"			: 1,
		"movement speed": 1.06,
		"intellect"		: 1
	}

	def __init__(self, name, level = 1, difficulty = 1):
		""" Creates an eagle """
		super(Eagle, self).__init__(name, level, difficulty)
		self.modifiers = {		# modifiers for equipment
			"melee"				: 1.2,
			"melee defense"		: 1.1,
			"ranged"			: 1.2,
			"ranged defense"	: 1.0,
			"magic"				: 0,
			"defense"			: 1,
			"magic defense"		: 1,
			"fire resistance"	: 2,
			"ice resistance"	: 2,
			"speed"				: 1.5
		}

		self.statistics_base = {
			"health"		: 65 +  (15 * difficulty),
			"attack"		: 135 +  (25 * difficulty),
			"endurance"		: 100 +  (20 * difficulty),
			"vitality"		: 80  +  (8 * difficulty),
			"mana"			: 100 +  (4 * difficulty),
			"movement speed": 150 +  (20 * difficulty),
			"intellect"		: 100 +  (5 * difficulty)
		}

		for key in self.statistics_base:
			self.statistics_base[key] = (self.statistics_base[key]
									* (self.level_modifier[key] ** level))
		self.current_health = self.statistics_base["health"]
		self.current_mana = self.statistics_base["mana"]

		self.inventory = list()
		self.inventory.append(Weapon.FireAndIceCrossBows(2,10,True))

		self.drops = {
			"experience" 	: 60 * level,
			"gold"			: 65 * level,
			"items"			: self.inventory
		}

class DireWolf(Monster):
	class_name = "dire wolf"
	desc = "\ta large wolf, capable of leading any pack"
	aptitude = ("\tparticularly fast and aggressive")
	level_modifier = { 	# modifiers applied on level
		"health"		: 1.02,
		"attack"		: 1.11,
		"endurance"		: 1.01,
		"vitality"		: 1.05,
		"mana"			: 1,
		"movement speed": 1.08,
		"intellect"		: 1
	}

	def __init__(self, name, level = 1, difficulty = 1):
		""" Creates a dire wolf """
		super(DireWolf, self).__init__(name, level, difficulty)
		self.modifiers = {		# modifiers for equipment
			"melee"				: 1.3,
			"melee defense"		: 1,
			"ranged"			: 1.1,
			"ranged defense"	: 0.8,
			"magic"				: 0,
			"defense"			: 1,
			"magic defense"		: 1,
			"fire resistance"	: .5,
			"ice resistance"	: 2,
			"speed"				: 1.5
		}

		self.statistics_base = {
			"health"		: 55 +  (15 * difficulty),
			"attack"		: 140 +  (25 * difficulty),
			"endurance"		: 100 +  (20 * difficulty),
			"vitality"		: 80  +  (8 * difficulty),
			"mana"			: 100 +  (4 * difficulty),
			"movement speed": 135 +  (20 * difficulty),
			"intellect"		: 100 +  (5 * difficulty)
		}

		for key in self.statistics_base:
			self.statistics_base[key] = (self.statistics_base[key]
									* (self.level_modifier[key] ** level))
		self.current_health = self.statistics_base["health"]
		self.current_mana = self.statistics_base["mana"]

		self.inventory = list()
		self.inventory.append(Weapon.FireAndIceCrossBows(2,10,True))

		self.drops = {
			"experience" 	: 50 * level,
			"gold"			: 30 * level,
			"items"			: self.inventory
		}

# quick access to each type of Monster
TYPES = {
	"goblin" 		: Goblin,
	"dragon" 		: Dragon,
	"giant eagle"	: Eagle,
	"dire wolf"		: DireWolf
}