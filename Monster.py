import random
import Weapon
from Shared import *

class Monster(object):
	difficulty_level = ("easy", "normal", "exceptional")

	def __init__(self, name, level = 1, difficulty = 1):
		self.name = name
		self.difficulty = difficulty
		self.level = level
		self.alive = True
		self.equipped_weapon = None

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
			print ("you dealt " + str(int(round(overall_damage))) + " damage")
			if(self.current_health <= 0):
				self.current_health = 0
				self.alive = False
				print(self.name + " died")
				print("")
				return self.drops
			else:
				if(damage_calc > 0):
					print(self.name + " survived the hit")
				else:
					print(self.name + " was not affected")
		else:
			print("attacking the dead creature has no effect")

	def level_up(self):
		if (self.level < 100):
			self.level += 1
			for key, value in self.statistics_base.items():
				self.statistics_base[key] = value * self.level_modifier[key]

	def __repr__(self):
		return (self.class_name + "(" + self.name + ", " + 
						self.level + ", " + self.difficulty + ")")

	def __str__(self):
		return self.name + " the " + self.class_name.lower()

	def get_attack(self, isRanged = False, isMagic = False):
		if (self.equipped_weapon != None):
			attack_base = self.equipped_weapon.get_attack()
		else:
			attack_base = (0, 0, 0, 0)
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


class Goblin(Monster):
	class_name = "Goblin"
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

		self.items = list()
		sword = Weapon.LongSword(1, 2, True)
		self.items.append(sword)
		self.equipped_weapon = sword
		self.drops = {
			"experience" 	: 45 * level,
			"gold"			: 25 * level,
			"items"			: self.items
		}

class Dragon(Monster):
	class_name = "Dragon"
	desc = "\ta large conglomeration of a snake and a serpent"
	aptitude = ("\tGreatly resitant to fire")
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
		super(Dragon, self).__init__(name, level, difficulty)
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

		self.items = list()
		self.items.append(Weapon.FireAndIceCrossBows(2,10,True))

		self.drops = {
			"experience" 	: 100 * level,
			"gold"			: 90 * level,
			"items"			: self.items
		}

TYPES = {
	"goblin" : Goblin,
	"dragon" : Dragon
}