import Monster
import Weapon
import Player
from Shared import *

def check_loot (drops, player):
	if (drops != None):
		player.give_exp(drops["experience"])
		player.gold += drops["gold"]
		print("the monster dropped " + str(drops["gold"]) + " gold!")

		for item in drops["items"]:
			response = prompt_for ("take " + str(item) + "?",
							("Yes", "No"))
			if (response.upper() == "YES"):
				player.inventory.append(item)
				print("you stashed the item in your inventory")

def game_over(player):
	if(not player.alive):
		print("you died, game over :(")

def fight(enemy, player):
	print("fighting " + str(enemy))
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


player_name = input("what's your name? ")
print("")
class_choice = prompt_for("which class do you want to play as? ",
								tuple(Player.CLASSES.keys()))
player = Player.CLASSES[class_choice](player_name)
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
			move = prompt_for("", ("display inventory", "equip item", "view equipped item",
									"fight the dragon", "fight a goblin", "fight a random enemy",
									"cheat"))

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
			elif (move.lower() == "fight a random enemy"):
				fight(Monster.get_random_enemy(tuple(Monster.TYPES.keys()), ("rando"), 0, 10, 0, 2),
							player)
			elif (move.lower() == "view equipped item"):
				player.view_equipped()
