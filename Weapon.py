import random

def random_range(base_value, percent_range):
	value_bonus = random.randint(0, percent_range + 1)
	output = base_value - (base_value * (percent_range / 2) / 100)
	return output + (value_bonus * base_value / 100)

class Weapon(object):
	weapon_prefixes = (
		"cutting",
		"accurate",
		"weak",
		"strong",
		"heavy",
		"light",
		"enflamed",
		"frosty"
	)

	prefix_desc = { # this weapon...
		"cutting" : "is surprisingly sharp",
		"accurate" : "is said to always find it's target",
		"weak" : "the first weapon ever made by a master blacksmith",
		"strong" : "compensates for it's user's lack of strength",
		"heavy" : "has a surprising heft to it",
		"light" : "could be used by a toddler",
		"enflamed" : "belonged to a pyromanrriac",
		"frosty" : "has been used as a bar trick one too many times"
	}

	quality_level = (
		"poor",
		"average quality",
		"high end",
		"exceptional"
	)

	def __init__(self, quality, level = 0, prefix = False, prefix_given = None):
		self.quality = quality
		self.level = level
		self.prefix = None
		if (prefix):
			if (prefix_given != None):
				self.prefix = prefix_given
			else:
				self.prefix = random.choice(self.weapon_prefixes)
		self.stats = {
			"close_range" : 0,
			"long_range" : 0,
			"fire" : 0,
			"ice" : 0,
			"defense" : 0,
			"critical" : 0,
			"accuracy" : 0,
			"weight" : 0,
			"speed" : 0
		}

	def __repr__(self):
		output = self.quality_level[self.quality] + " "

		if self.prefix != None:
			output += self.prefix + " "
		output += self.class_name
		if self.level != 0:
			output += " +" + str(self.level)
		return output

	def get_desc(self):
		output = "\ta " + self.quality_level[self.quality] + " quality " + self.__repr__()
		output += "\n\t" + self.desc
		if self.prefix != None:
			output += "\n\tthis weapon " + self.prefix_desc[self.prefix]
		return output + "\n"

	def get_save(self):
		output = (
			self.class_name,
			self.prefix,
			self.quality,
			self.level
		)
		return output

	def upgrade(self):
		if self.level < 10:
			self.stats["close_range"] *= 1.1
			self.stats["long_range"] *= 1.1
			self.stats["fire"] *= 1.1
			self.stats["ice"] *= 1.1
			self.stats["critical"] += 1.5
			self.level += 1
			return True
		else:
			return False

	def get_level_modif(self, num_upgrades):
		setTo = self.level
		self.level = 0
		for x in range(0, setTo):
			self.upgrade()

	def get_prefix_effect(self):
		if self.prefix == None:
			return None
		if self.prefix == "cutting":
			self.stats["close_range"] *= 1.15
		elif self.prefix == "accurate":
			self.stats["accuracy"] *= 1.15
		elif self.prefix == "weak":
			self.stats["close_range"] *= .85
			self.stats["long_range"] *= .85
			self.stats["defense"] *= .75
			self.stats["fire"] *= .85
			self.stats["close_range"] *= 1.3
			self.stats["ice"] *= .85
		elif self.prefix == "strong":
			self.stats["long_range"] *= 1.3
			self.stats["defense"] *= 1.2
			self.stats["accuracy"] *= .8
		elif self.prefix == "heavy":
			self.stats["weight"] *= 1.15
			self.stats["long_range"] *= 1.25
			self.stats["close_range"] *= 1.25
			self.stats["accuracy"] *= 1.1
			self.stats["speed"] *= .7
			self.stats["defense"] *= 1.2
		elif self.prefix == "light":
			self.stats["weight"] *= .8
			self.stats["long_range"] *= .95
			self.stats["close_range"] *= .9
			self.stats["accuracy"] *= 1.1
			self.stats["speed"] *= 1.3
			self.stats["defense"] *= 1.2
		else:
			total_ar = self.stats["close_range"] + self.stats["long_range"]
			total_ar += self.stats["fire"] + self.stats["ice"]
			if self.prefix == "enflamed":
				self.stats["fire"] += .25 * total_ar
			elif self.prefix == "frosty":
				self.stats["ice"] += .25 * total_ar

	def get_quality_modif(self):
		modifier = 0
		if self.quality == 0:
			modifier = .75
		elif self.quality == 1:
			modifier = .9
		elif self.quality == 2:
			modifier = 1
		elif self.quality == 3:
			modifier = 1.25
		for keys in self.stats:
			self.stats[keys] *= modifier

	def get_attack(self):
		if random.randint(0,100) > self.stats["accuracy"]:
			return (0,0,0,0)

		modifier = 1.5 if random.randint(0,100) < self.stats["critical"] else 1
		modifier *= (random.randint(0, 30) + 85) / 100

		output = (
			int(round(self.stats["close_range"] * modifier)),
			int(round(self.stats["long_range"] * modifier)),
			int(round(self.stats["fire"] * modifier)),
			int(round(self.stats["ice"] * modifier))
		)
		return output

	def get_attack_value(self, attack):
		output = 0;
		for values in attack:
			output+= values
		return output


	def get_stats(self):
		print("stats for " + self.__repr__())
		print("\tclose range damage:     " + str(int(round(self.stats["close_range"]))))
		print("\tlong range damage:      " + str(int(round(self.stats["long_range"]))))
		print("\tfire damage:            " + str(int(round(self.stats["fire"]))))
		print("\tice damage:             " + str(int(round(self.stats["ice"]))))
		print("\tdefense:                " + str(int(round(self.stats["defense"]))))
		print("\tcritical hit chance:    " + str(int(round(self.stats["critical"]))))
		print("\taccuracy:               " + str(int(round(self.stats["accuracy"]))))
		print("\tweight:                 " + str(int(round(self.stats["weight"]))))
		print("\tspeed:                  " + str(int(round(self.stats["speed"]))))
		print("")


# weapons
class LongSword(Weapon):
	class_name = "longsword"
	desc = "a sword designed to be usable with either one hand or two"

	def __init__(self, quality, level = 0, prefix = False, prefix_given = None):
		super(LongSword, self).__init__(quality, level, prefix, prefix_given)
		self.stats["close_range"] = 50
		self.stats["accuracy"] = 90
		self.stats["weight"] = 6.5
		self.stats["critical"] = 6
		self.stats["speed"] = 65
		self.stats["defense"] = 35
		self.get_prefix_effect()
		self.get_quality_modif()
		self.get_level_modif(level)

class DualCrossBows(Weapon):
	class_name = "dual cross bows"
	desc = "a pair of crossbows intended to vanquish evil"
	
	def __init__(self, quality, level = 0, prefix = False, prefix_given = None):
		super(DualCrossBows, self).__init__(quality, level, prefix, prefix_given)
		self.stats["long_range"] = 40
		self.stats["accuracy"] = 90
		self.stats["weight"] = 3
		self.stats["critical"] = 15
		self.stats["speed"] = 90
		self.get_prefix_effect()
		self.get_quality_modif()
		self.get_level_modif(level)

class FireAndIceCrossBows(DualCrossBows):
	class_name = "special dual cross bows"
	desc = "a pair of crossbows intended to vanquish evil with fire and ice"
	
	def __init__(self, quality, level = 0, prefix = False, prefix_given = None):
		super(FireAndIceCrossBows, self).__init__(quality, level, prefix, prefix_given)
		bonus = 15
		for x in range(0,level):
			bonus *= 1.1
		self.stats["fire"] += bonus
		self.stats["ice"] += bonus
		self.stats["long_range"] = bonus

TYPES = {
	"longsword" : LongSword,
	"dual crossbows" : DualCrossBows,
	"special dual crossbows" : FireAndIceCrossBows
}