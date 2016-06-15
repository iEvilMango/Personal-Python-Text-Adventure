import Weapon
import Monster
import random
from Shared import *

class Player(Character):
	def __init__(self, name, level = 1, inventory = list()):
		self.name = name
		self.level = level
		self.alive = True

		self.inventory = inventory
		self.gold = 1000
		self.experience = 0
		self.drops = {
			"experience" 	: 1000,
			"gold"			: self.gold,
			"items"			: self.inventory
		}

	def deal_damage(self, damage):
		return super(Player, self).deal_damage(damage, "the dead body of " + self.name + " was attacked")

	def level_up(self):
		super(Player, self).level_up(True)

	def give_exp(self, amount):
		super(Player, self).give_exp(amount, True)

	def __repr__(self):
		return (self.class_name + "(" + self.name + ", " + self.level + ", " +
					 repr(self.inventory) + ")")

	def __str__(self):
		return self.name + " the " + self.class_name.lower()

	def display_inventory(self):
		super(Player, self).display_inventory(True)

	def equip_item(self):
		super(Player, self).equip_item()

class Warrior(Player):
	class_name = "Warrior"
	desc = "\ta warrior pledged to defend all against evil"
	aptitude = "\tparticularly good with close ranged combat"

	level_modifier = { 	# modifiers applied on level
		"health"		: 1.06,
		"attack"		: 1.06,
		"endurance"		: 1.02,
		"vitality"		: 1.08,
		"mana"			: 1.03,
		"movement speed": 1.05,
		"intellect"		: 1.01
	}

	def __init__(self, name, level = 1, inventory = list()):
		super(Warrior, self).__init__(name, level, inventory)
		self.modifiers = {		# modifiers for equipment
			"melee"				: 1.2,
			"melee defense"		: 1.3,
			"ranged"			: .5,
			"ranged defense"	: .5,
			"magic"				: .5,
			"defense"			: 1,
			"magic defense"		: .9,
			"fire resistance"	: .75,
			"ice resistance"	: .75,
			"speed"				: 1.2
		}

		self.statistics_base = {
			"health"		: 100,	# health points
			"attack"		: 125,	# attack bonus
			"endurance"		: 80,	# defense bonus
			"vitality"		: 60,	# ability to perform successive attacks w/o wearing out
			"mana"			: 70,	# mana points
			"movement speed": 90,	# how quickly they move
			"intellect"		: 85	# Bonus to magic attack, intelligence checks
		}

		for key in self.statistics_base:
			self.statistics_base[key] = (self.statistics_base[key]
									* (self.level_modifier[key] ** level))
		self.current_health = self.statistics_base["health"]
		self.current_mana = self.statistics_base["mana"]

		self.inventory.append(Weapon.LongSword(1, 0, False))
		self.equipped_weapon = self.inventory[0]

class Monk(Player):
	class_name = "Monk"
	desc = "\ta religious figure dedicated to eradicating all monsters."
	aptitude = "\tparticularly good with fighting with their hands"

	level_modifier = { 	# modifiers applied on level
		"health"		: 1.07,
		"attack"		: 1.09,
		"endurance"		: 1.01,
		"vitality"		: 1.05,
		"mana"			: 1.04,
		"movement speed": 1.05,
		"intellect"		: 1.05
	}
	
	def get_attack(self):
		if(self.equipped_weapon == None):
			self.statistics_base["attack"] *= 2
		damage = super(Monk, self).get_attack()
		if(self.equipped_weapon == None):
			self.statistics_base["attack"] /= 2
		return damage

	def __init__(self, name, level = 1, inventory = list()):
		super(Monk, self).__init__(name, level, inventory)
		self.modifiers = {		# modifiers for equipment
			"melee"				: 1.3,
			"melee defense"		: 1.3,
			"ranged"			: .25,
			"ranged defense"	: .25,
			"magic"				: .25,
			"defense"			: 1.2,
			"magic defense"		: .9,
			"fire resistance"	: 1.2,
			"ice resistance"	: .6,
			"speed"				: 1.4
		}

		self.statistics_base = {
			"health"		: 110,	# health points
			"attack"		: 145,	# attack bonus
			"endurance"		: 70,	# defense bonus
			"vitality"		: 40,	# ability to perform successive attacks w/o wearing out
			"mana"			: 30,	# mana points
			"movement speed": 110,	# how quickly they move
			"intellect"		: 95	# Bonus to magic attack, intelligence checks
		}

		for key in self.statistics_base:
			self.statistics_base[key] = (self.statistics_base[key]
									* (self.level_modifier[key] ** level))
		self.current_health = self.statistics_base["health"]
		self.current_mana = self.statistics_base["mana"]

		self.equipped_weapon = None

CLASSES = {
	"warrior" : Warrior,
	"monk" : Monk
}