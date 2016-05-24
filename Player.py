import Weapon
import Monster
import random
from Shared import *

class Player(object):
	
	def __init__(self, name, level = 1, inventory = list()):
		self.name = name
		self.level = level
		self.alive = True

		# self.inventory = list()
		self.inventory = inventory
		self.gold = 1000
		self.experience = 0

	def get_desc(self):
		return self.name + " is a " + self.class_name + "\n" + self.desc

	def examine(self):
		print("an examination of " + self.name + " reveals: ")
		print(self.aptitude)
		print("\thealth points:          " + str(int(round(self.current_health)))
								   + " / " + str(int(round(self.statistics_base["health"]))))
		print("\tmana points:            " + str(int(round(self.current_mana)))
								   + " / " + str(int(round(self.statistics_base["mana"]))))
		print("\tendurance:              " + str(int(round(self.statistics_base["health"]))))
		print("\tvitality:               " + str(int(round(self.statistics_base["health"]))))
		print("\tmovement speed:         " + str(int(round(self.statistics_base["movement speed"]))))
		print("\tintellect:              " + str(int(round(self.statistics_base["intellect"]))))

	def deal_damage(self, damage):
		if(self.alive):
			damage_calc = damage[0] / self.modifiers["melee defense"]
			damage_calc += damage[1] / self.modifiers["ranged defense"]
			damage_calc += damage[2] / self.modifiers["fire resistance"]
			damage_calc += damage[3] / self.modifiers["ice resistance"]

			overall_damage = damage_calc * 100 / self.statistics_base["endurance"]
			self.current_health -= overall_damage
			print (self.name + " was dealt " + str(int(round(overall_damage))) + " damage")

			if(self.current_health <= 0):
				self.current_health = 0
				self.alive = False
				print(self.name + " died")
			else:
				if(damage_calc > 0):
					print(self.name + " survived the hit")
				else:
					print(self.name + " was not affected")
		else:
			print("the dead body of " + self.name + " was attacked")

	def level_up(self):
		if (self.level < 100):
			self.level += 1
			print(self.name + " leveled up to level " + str(self.level))
			for key, value in self.statistics_base.items():
				self.statistics_base[key] = value * self.level_modifier[key]

			self.current_health = self.statistics_base["health"]
			self.current_mana = self.statistics_base["mana"]

	def give_exp(self, amount):
		print(self.name + " gained " + str(amount) + " experience!")
		while (amount > 0):
			experience_needed = 100 * self.level - self.experience
			if (amount >= experience_needed):
				amount -= experience_needed
				self.level_up()
				self.experience = 0
			else:
				self.experience += amount
				amount = 0

	def __repr__(self):
		return (self.class_name + "(" + self.name + ", " + self.level + ", " +
					 repr(self.inventory) + ")")

	def __str__(self):
		return self.name + " the " + self.class_name.lower()

	def display_inventory(self):
		print(self.name + "'s inventory")
		print("\tgold: " + str(self.gold))
		for item in self.inventory:
			print ("\t" + str(item))

	def equip_item(self):
		if(len(self.inventory) > 0):
			available_items = []
			corresponding_index = {}
			count = 0
			for item in self.inventory:
				available_items.append(str(item))
				corresponding_index[str(item)] = count
				count +=1
			choice = prompt_for("change " + self.name + "'s equipped item to what?",
									available_items)

			equipped_weapon = self.inventory[corresponding_index[choice]]
			print(self.name + " equipped " + str(equipped_weapon))
		else:
			print("inventory is empty")


	def get_attack(self, isRanged = False, isMagic = False):
		attack_base = self.equipped_weapon.get_attack()
		melee_bonus = 0
		if (not isRanged):
			melee_bonus = self.statistics_base["attack"]

		ranged_bonus = 0
		if (isRanged):
			ranged_bonus = self.statistics_base["attack"]

		fire_bonus = 0
		if (isMagic and attack_base[2] != 0):
			fire_bonus = self.statistics_base["intellect"]

		ice_bonus = 0
		if (isMagic and attack_base[3] != 0):
			ice_bonus = self.statistics_base["intellect"]

		output = (
			int(round(attack_base[0] * self.modifiers["melee"] 
						+ melee_bonus)),
			int(round(attack_base[1] * self.modifiers["ranged"]
						+ ranged_bonus)),
			int(round(attack_base[2] * self.modifiers["magic"]
						+ fire_bonus)),
			int(round(attack_base[3] * self.modifiers["magic"]
						+ ice_bonus))
		)
		return output

	def print_battle_stats(self):
		print("updated health for " + self.name)
		print("\thealth points:          " + str(int(round(self.current_health)))
								   + " / " + str(int(round(self.statistics_base["health"]))))
		print("\tmana points:            " + str(int(round(self.current_mana)))
								   + " / " + str(int(round(self.statistics_base["mana"]))))

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

CLASSES = {
	"warrior" : Warrior
}