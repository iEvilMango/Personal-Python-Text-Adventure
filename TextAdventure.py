import Monster
import Weapon
import Player

def prompt_for(prompt, valid_responses):
	while(True):
		print (prompt)
		options = ""
		for item in valid_responses:
			options += "[" + str(item) + "] "
		print(options)

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

def check_loot (drops, player):
	if (drops != None):
		player.give_exp(drops["experience"])
		player.gold += drops["gold"]
		print("the monster dropped " + str(drops["gold"]) + " gold!")

		for item in drops["items"]:
			response = prompt_for ("take " + item.__repr__() + "?",
							("Yes", "No"))
			if (response.upper() == "YES"):
				player.inventory.append(item)
				print("you stashed the item in your inventory")

def game_over(player):
	if(not player.alive):
		print("you died, game over :(")

def fight(enemy, player):
	print("fighting " + enemy.__repr__())
	while(enemy.alive and player.alive):
		player.print_battle_stats()
		
		response = prompt_for("What do you want to do? " + enemy.name + " is waiting... ",
								("attack", "examine enemy", "nothing"))

		storage = None
		if(response.lower() == "attack"):
			storage = enemy.deal_damage(player.get_attack())
			check_loot(storage, player)
		elif(response.lower() == "examine enemy"):
			enemy.examine()
		elif(response.lower() == "nothing"):
			print ("the enemy is sad, they wanted to be attacked")

		print("")
		if(enemy.alive):
			player.deal_damage(enemy.get_attack())

		print("")
		game_over(player)


#inventory = []
#experience = 0
#gold = 0

player_name = input("What's your name? ")
print("")

# player = Player.Warrior(player_name)
player = Player.CLASSES["warrior"](player_name)
player.give_exp(1000)
player.inventory.append(Weapon.TYPES["special dual crossbows"](1, 3, True))
player.display_inventory()

move = "None don't work here"
print("current max of 100 turns")
for x in range(0,100):
	if (player.alive):
		move = "None don't work here"
		while (move.lower() != "fight the dragon" and move.lower() != "fight a goblin"):
			print("what next?")
			move = prompt_for("", ("display inventory", "equip item",
									"fight the dragon", "fight a goblin", "cheat"))

			if (move.lower() ==  "display inventory"):
				player.display_inventory()
			elif (move.lower() == "equip item"):
				player.equip_item()
			elif (move.lower() == "cheat"):
				player.give_exp(100000)
				weapon = Weapon.TYPES["longsword"](3, 10, True)
				player.inventory.append(weapon)
			elif (move.lower() == "fight the dragon"):
				fight(Monster.TYPES["dragon"]("dragosan", 10, 1), player)
			elif (move.lower() == "fight a goblin"):
				fight(Monster.TYPES["goblin"]("gobbinmon"), player)