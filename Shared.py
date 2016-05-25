def prompt_for(prompt, valid_responses):
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
	value_bonus = random.randint(0, percent_range + 1)
	output = base_value - (base_value * (percent_range / 2) / 100)
	return output + (value_bonus * base_value / 100)

class Character(object):
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

	def print_battle_stats(self):
		print("updated health for " + self.name)
		print("\thealth points:          " + str(int(round(self.current_health)))
								   + " / " + str(int(round(self.statistics_base["health"]))))
		print("\tmana points:            " + str(int(round(self.current_mana)))
								   + " / " + str(int(round(self.statistics_base["mana"]))))

	def deal_damage(self, damage, responseIfDead = ""):
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
				return self.drops
			else:
				if(damage_calc > 0):
					print(self.name + " survived the hit")
				else:
					print(self.name + " was not affected")
		else:
			print(responseIfDead)