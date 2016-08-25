import random

def prompt_for(prompt, valid_responses):
	"""
	Prompt user for one of the given responses. Allows for partial matches,
	and reprompts when given an invalid response. An input of quit (assuming
	quit does not match or partially match a response) will exit the game.
	"""
	while(True):
		print (prompt)
		options = ""
		for item in valid_responses:
			options += "[" + str(item) + "] "
		print(options) # [1,2,3]  => [1] [2] [3]

		response = input("")
		for possible in valid_responses:
			if (str(response).lower() == str(possible).lower()):
				return possible

		for possible in valid_responses:
			if (str(response).lower() in str(possible).lower()):
				return possible

		if (str(response).lower() == "quit"):
			quit()
		print(str(response) + " is not a valid input, try again, or [quit]")

def random_range(base_value, percent_range):
	"""
	Given a value, this will generate a value within +- half the
	given percent range
	"""
	value_bonus = random.randint(0, percent_range + 1)
	output = base_value - (base_value * (percent_range / 2) / 100)
	return output + (value_bonus * base_value / 100)

def getRoundedStr(input, decimals = 0):
	"""
	Converts an integer to a rounded value represented as a string.
	Optional decimals parameter allows for control over how much value is rounded;
	1 rounds to the tenths, -1 to the tens.
	When decimals is 0 or less (i.e. rounded to the ones place or higher),
	leaves string as an Integer; otherwise, represents string as a double.
	"""
	round_value = 10 ** decimals
	return_value = int(round(input * (round_value))) / round_value
	return_value = return_value if decimals > 0 else int(return_value)
	return str(return_value)


### todo: add "special attack / move" dict to allow for bonus options ###
class Character(object):
	"""
	Character object represents characters; that currently includes Players,
	Monsters, etc.
	"""
	def get_attack(self, isRanged = False, isMagic = False):
		"""
		Generates an attack from the character. Optional isRanged and
		isMagic attacks allow for customization of how stats are applied.
		"""
		if (self.equipped_weapon != None):
			attack_base = self.equipped_weapon.get_attack()
			if ((attack_base) == (0, 0, 0, 0)):
				return attack_base
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

	def print_battle_stats(self):
		"""
		Prints to console the characters health and mana
		"""
		print("updated stats for " + self.name)
		print("\thealth points:          " + str(int(round(self.current_health)))
								   + " / " + str(int(round(self.statistics_base["health"]))))
		print("\tmana points:            " + str(int(round(self.current_mana)))
								   + " / " + str(int(round(self.statistics_base["mana"]))))

	def deal_damage(self, damage, responseIfDead = ""):
		"""
		Deals damage to the character. Optional responseIfDead String 
		represents what is displayed if the character is already dead.
		"""
		if(self.alive):
			damage_calc = damage[0] / self.modifiers["melee defense"]
			damage_calc += damage[1] / self.modifiers["ranged defense"]
			damage_calc += damage[2] / self.modifiers["fire resistance"]
			damage_calc += damage[3] / self.modifiers["ice resistance"]

			overall_damage = damage_calc * 100 / self.statistics_base["endurance"] / 10
			overall_damage *= (random.randint(0, 30) + 85) / 100

			self.current_health -= overall_damage
			print (self.name + " was dealt " + str(int(round(overall_damage))) + " damage")

			if(self.current_health <= 0):
				self.current_health = 0
				self.alive = False
				print(self.name + " died")
				return self.drops
			else:
				if(damage_calc > 0):
					print(self.name + " survived the hit")
				else:
					print(self.name + " was not affected")
		else:
			print(responseIfDead)

	def level_up(self, printOnLevel = False):
		"""
		Levels up the character if possible, updating stats as necessary.
		Optional PrintOnLevel parameter will print to the console that the 
		character leveled up.
		"""
		if (self.level < 100):
			self.level += 1
			if(printOnLevel):
				print(self.name + " leveled up to level " + str(self.level))
			for key, value in self.statistics_base.items():
				self.statistics_base[key] = value * self.level_modifier[key]

			self.current_health = self.statistics_base["health"]
			self.current_mana = self.statistics_base["mana"]

	def give_exp(self, amount, printOnGain = False):
		"""
		gives experience to the character, leveling up as necessary.
		"""
		if(printOnGain):
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

	def display_inventory(self, hasGold = False):
		"""
		prints to console all items in characters inventory;
		optional hasGold parameter will add in how much gold they
		have as well.
		"""
		print(self.name + "'s inventory")
		if(hasGold):
			print("\tgold: " + str(self.gold))
		for item in self.inventory:
			print ("\t" + str(item))

	def equip_item(self):
		"""
		displays all items in characters inventory, allowing them to equip 
		them as weapons (some may be better than others.) Prompt also allows
		user to equip them with nothing.
		"""
		if(len(self.inventory) > 0):
			available_items = []
			corresponding_index = {}
			available_items.append("nothing")
			corresponding_index["nothing"] = 0
			count = 1
			for item in self.inventory:
				available_items.append(str(item))
				corresponding_index[str(item)] = count
				count += 1
			choice = prompt_for("change " + self.name + "'s equipped item to what?", available_items)

			if(choice == "nothing"):
				self.equipped_weapon = None
				print(self.name + " now has no weapon equipped")
			else:
				self.equipped_weapon = self.inventory[corresponding_index[choice] - 1]
				print(self.name + " equipped " + str(self.equipped_weapon))
		else:
			print("inventory is empty")

	def examine(self):
		"""
		examines the character, displaying all stats, as well as the
		characters aptitude.
		"""
		print("an examination of " + self.name + " reveals: ")
		print(self.aptitude)
		print("\thealth points:          " + getRoundedStr(self.current_health)
								   + " / " + getRoundedStr(self.statistics_base["health"]))
		print("\tmana points:            " + getRoundedStr(self.current_mana)
								   + " / " + getRoundedStr(self.statistics_base["mana"]))
		print("\tendurance:              " + getRoundedStr(self.statistics_base["health"]))
		print("\tvitality:               " + getRoundedStr(self.statistics_base["health"]))
		print("\tmovement speed:         " + getRoundedStr(self.statistics_base["movement speed"]))
		print("\tintellect:              " + getRoundedStr(self.statistics_base["intellect"]))

	def get_desc(self):
		""" returns a description of the character. """
		return self.name + " is a " + self.class_name + "\n" + self.desc

	def view_equipped(self):
		""" prints to console what the character has equipped. """
		if(self.equipped_weapon == None):
			print(self.name + " has nothing equipped")
		else:
			print(self.name + " has " + str(self.equipped_weapon) + " equipped")