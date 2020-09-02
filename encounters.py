from random import randint
from random import choice

######### OBJECTS ###############

class EnemyMaker(object):
    def __init__(self, species):
        self.species = species
        if self.species == "ground":
            self.entrance_verb = "charges forward"
            self.attack_verb = "lunges"
            self.get_stats()
        elif self.species == "flying":
            self.entrance_verb = "swoops in"
            self.attack_verb = "dives"
            self.get_stats()

    def get_stats(self):
        if self.species == "ground":
            self.name = choice(["panther", "unicorn", "ogre", "wolf", "python"])
            self.health = randint(9,12)
        elif self.species == "flying":
            self.name = choice(["bat", "hawk", "owl", "swarm of pixies", "phoenix"])
            self.health = randint(11,14)

class Player(object):
    def __init__(self, name):
        self.name = name
        self.health = 25
        self.max_health = 25
        self.spider_bites = 0
        self.inventory = {
            "potion": 0,
            "bandage": 0,
        }

# will "equip" relevant weapons to player after they make their character choice
class Weapon(object):
  def __init__(self, name, ground_damage, flying_damage):
    self.name = name
    self.ground_damage = ground_damage
    self.flying_damage = flying_damage

# stores all of the actions (both enemy and player) available during the battle sequence
class BattleAction(object):
    def __init__(self):
        pass

    def initiate_battle(self):
        print("\n++++++++++++++++++++++++++++++++++++++++++\n")
        print(f"{enemy.name.upper()} {enemy.entrance_verb}!\n")

    def attack_player(self):
        self.damage_to_player = randint(1,5)
        player.health -= self.damage_to_player
        print (f">>>>>>>>>> {enemy.name.upper()} {enemy.attack_verb} at you for {self.damage_to_player} damage!\n")

    def attack_enemy(self, weapon, enemy_type):
        if enemy_type == "ground":
            damage_to_enemy = weapon.ground_damage
        if enemy_type == "flying":
            damage_to_enemy = weapon.flying_damage
        enemy.health -= damage_to_enemy
        print(f"Used {weapon.name.upper()} on {enemy.name.upper()} for {damage_to_enemy} damage! <<<<<<<<<<\n")

    def apply_bandage(self):
        player.health += 5
        player.inventory['bandage'] -= 1
        print("Applied BANDAGE to increase your health by 5! <<<<<<<<<<\n")

    def try_to_run(self):
        run_odds = randint(1,3)
        if run_odds >= 2:
            player.able_to_run = True
        if run_odds == 1:
            print("You trip while attempting to flee. <<<<<<<<<<\n")

# holds the indv steps that makes each battle sequence happen, plus the ability to run all of those steps
class BattleMaker(object):
    def __init__(self):
        self.is_active = True
        self.run_battle_sequence()

    def display_battle_menu(self):
        print("=================================\n")
        print(f"Your health: {player.health}")
        print(f"Enemy health: {enemy.health}")
        print(f"Bandage count: {player.inventory['bandage']}")
        print(f"Life potion count: {player.inventory['potion']}")

        print("\nAvailable actions:")
        print(f"  1 {player.primary_weapon.name.upper()}")
        print(f"  2 {player.secondary_weapon.name.upper()}")
        print("  3 RUN")
        if player.inventory['bandage'] > 0:
            print("  4 APPLY BANDAGE")
        print("\n=================================\n")

    def get_player_action(self):
        while True:
            action_num = input("Choose an action: ")
            if action_num == "1":
                return player.primary_weapon
            if action_num == "2":
                return player.secondary_weapon
            if action_num == "3":
                return "run"
            if player.inventory['bandage'] > 0 and action_num == "4":
                return "bandage"
        # will keep prompting until player enters valid option. once they do, the return will break the while loop/break out of the function

    def take_player_action(self, player_action_choice):
        player_action = BattleAction()
        if player_action_choice == "run":
            player_action.try_to_run()
        elif player_action_choice == "bandage":
            player_action.apply_bandage()
        else:
            player_action.attack_enemy(player_action_choice, enemy.species)

    def end_battle(self):
        if enemy.health <= 0:
            print(f">>>>>>>>>> {enemy.name.upper()} is defeated and scatters away!\n")
            print("You catch your breath and survey your wounds.")
            print(f"Your health: {player.health}\n")
            print("++++++++++++++++++++++++++++++++++++++++++\n")
        elif player.health <= 0:
            print(f">>>>>>>>>> {enemy.name.upper()} scatters away!\n")
            game_over_or_use_potion()
        elif player.able_to_run:
            print("You run from the encounter! <<<<<<<<<< ")
            print(f"Your health: {player.health}")
            print("\n++++++++++++++++++++++++++++++++++++++++++\n")

    def run_battle_sequence(self):
        enemy_action = BattleAction()
        enemy_action.initiate_battle()
        player.able_to_run = False

        while self.is_active:
            self.display_battle_menu()
            player_action_choice = self.get_player_action()
            print()
            self.take_player_action(player_action_choice)

            if enemy.health > 0 and player.able_to_run == False:
                enemy_action.attack_player()

            if enemy.health <= 0 or player.health <0 or player.able_to_run:
                self.is_active = False

        self.end_battle()

class Location(object):
    # visit_log stores every room player has gone to
    # way of randomizing future rooms by checking which rooms they've visited?
    visit_log = []

    def __init__(self, name):
        self.name = name

        # always room 1
        if self.name == "entrance hall":
            self.item = "potion"
            self.description = "As expected, it's dark in here."

        # room 2 if they choose left
        if self.name == "musty hallway":
            self.item = "bandage"
            self.description = "You wipe your forehead; this hallway is musty and humid. It's still too dark to see much."

        # room 2 if they choose right
        if self.name == "drafy hallway":
            self.item = "bandage"
            self.description = "You shiver; there's a chill in the air in this drafty hallway. It's still too dark to see much."

        # room 3 if they continue forward
        if self.name == "study":
            self.item = choice(["bandage", "bandage", "potion"])
            self.description = "There's a tiny window near the ceiling, letting in a dull, gray light.\nYou can just make out a small wooden desk in the corner.\nYou see a BOX perched on the edge of the desk.\n"

        # room 3 if they go through door
        if self.name == "library":
            self.item = choice(["bandage", "bandage", "potion"])
            self.description = "Your eyes begin to adjust to the dark.\nYou can just make out rows and rows of dusty bookshelves lining the walls of this room.\nThere's a small BOX perched on the edge of the nearest shelf.\n"

    def enter_room(self):
        Location.visit_log.append(self.name)
        print(self.description)


########### FUNCTIONS ############

def generate_enemy_type():
    enemy_type = choice(["flying", "ground"])
    return enemy_type

def game_over_or_use_potion():
  if player.inventory['potion'] <= 0:
    print("\nYour health: 0\n")
    print("....................\n")
    print("<><><><><><><>GAME OVER<><><><><><><>\n")
    print(quit)
    quit()
  else:
    print("\nYour health: 0\n")
    print("....................\n")
    print("You collapse on the ground.\n")
    print("Time for a life potion. Bottoms up.")
    player.inventory['potion'] -= 1
    player.health = player.max_health
    print(f"Life potions remaining: {player.inventory['potion']}")
    print ("\nYou feel a burst of light and energy and get to your feet.")
    print (f"Your health: {player.health}\n")
    print("++++++++++++++++++++++++++++++++++++++++++\n")

def continue_or_quit():
    while True:
        player_continue = input("Shall we continue? Y / N: ").upper()
        print ()
        if player_continue == "Y":
            print ("Let's go.\n")
            break
        if player_continue == "N":
            print (f"Not much of a {player.character} after all. Goodbye.\n")
            print (quit)
            quit()

def add_to_inventory(item):
    player.inventory[item] += 1
    print(f"{item.capitalize()} count: {player.inventory[item]}")

def open_box():
    box_item = choice(["potion", "bandage", "bandage", "bite"])
    if box_item != "bite":
        print("Nice find.")
        add_to_inventory(box_item)
    else:
        give_player_spider_bite()

def give_player_spider_bite():
    player.spider_bites +=1
    if player.spider_bites == 3:
        print("Oh no... your third bite!")
        game_over_or_use_potion()
    else:
        print("Watch out! Three bites and you're a goner!")
        print(f"Spider bites so far: {player.spider_bites}")






################### GAMEPLAY #################

######### PROLOGUE ##########

print("<><><><><> ENCHANTED ENCOUNTERS! <><><><><>")
print("  <><><><><> A TEXT ADVENTURE <><><><><>\n")

# initialize player
player_name = input("What is your name? ").title()
player = Player(player_name)

# set up character type and weapons
print(f"{player.name} is who you are in the real world.")
print("Who will you be today?\n")
print("WIZARDS are more effective against flying enemies.")
print("FIGHTERS are more effective against ground enemies.\n")

while True:
    player_character_choice = input("Enter W for WIZARD or F for FIGHTER: ").upper()

    if player_character_choice == "W":
        player.character = "wizard"
        player.primary_weapon = Weapon("magic spell", 1, 3)
        player.secondary_weapon = Weapon("bow", 2, 2)
        print("A wizard, eh?")
        print("If you say so.\n")
        break
    elif player_character_choice == "F":
        player.character = "fighter"
        player.primary_weapon = Weapon("sword", 3, 1)
        player.secondary_weapon = Weapon("darts", 2, 2)
        print("So you'll be a fighter.")
        print("Interesting choice.\n")
        break

########## FIRST ENCOUNTER ###########

continue_or_quit()

print("\n~~~~~~~~~~FIRST ENCOUNTER~~~~~~~~~~\n")

room1 = Location("entrance hall")
room1.enter_room()

print("\nYour boots brush against something on the ground in front of you.\n")

while True:
    pick_up_answer = input("Pick it up? Y / N: ").upper()
    if pick_up_answer == "Y":
        print("\nGood.")
        break
    if pick_up_answer == "N":
        print("\nThat's ridiculous. I've added it to your inventory anyway.")
        break

add_to_inventory(room1.item)

print("\nShould you meet your end, so to speak, these will revive you.\n")
print("Let's move on.\n")

print("You hear a rustle from somewhere in the darkness.")
print("Hmm, you're right to be tense. We're not alone.\n")
print("You do know how to defend yourself, yes?")

if player.character == "wizard":
  print("If it comes to it, you can use a magic spell or your bow and arrow.\n")

if player.character == "fighter":
  print("If it comes to it, you can use your sword or those darts you brought along.\n")

print("You continue onward, when suddenly--\n")

enemy = EnemyMaker(generate_enemy_type())
battle = BattleMaker()

print("Well, that was interesting.")
print("Now, where were we?\n")

print("You hear a 'drip drip drip' noise coming from the LEFT.")
print("You hear a 'whoosh whoosh whoosh' noise coming from the RIGHT.\n")

while True:
    left_or_right = input("Which way do you go? Enter L for left or R for right: ").upper()
    if left_or_right == "L":
        room2 = Location("musty hallway")
        break
    if left_or_right == "R":
        room2 = Location("drafty hallway")
        break

print()
room2.enter_room()

print("\nYou step forward and nearly trip over something.\n")

while True:
    pick_up_answer = input("Pick it up? Y / N: ").upper()
    if pick_up_answer == "N":
        print("\nHonestly. Why do I even ask.")
        print("With your attitude, how will we ever get out of here?\n")
        break
    if pick_up_answer == "Y":
        print("\nGood, very good.")
        print("We'll need these if we ever hope to get out of here.\n")
        break

add_to_inventory(room2.item)

print ("\nLet's hurry onward.\n")

####### INTO THE DARK #########

continue_or_quit()

print("\n~~~~~~~~~~INTO THE DARK~~~~~~~~~~\n")

print("You feel your way along the wall until you come to a DOOR.\n")

while True:
    door_answer = input("Go through it? Y / N: ").upper()
    if door_answer == "Y":
        room3 = Location("library")
        print("\nYou rattle the doorknob and manage to force the door open. You step through.\n")
        break
    if door_answer == "N":
        room3 = Location("study")
        print("\nYou ignore the door and continue into the room.\n")
        break

enemy = EnemyMaker(generate_enemy_type())
battle = BattleMaker()

print("You shake off the encounter and look around.\n")

room3.enter_room()

while True:
    open_box_answer = input("Open it? Y / N: ").upper()
    if open_box_answer == "N":
        print("\nI'll leave this one up to you.\n")
        break
    if open_box_answer == "Y":
        print()
        open_box()
        break


# print("You notice a piece of paper wedged under the box.\n")
# letters here



print("\nEND FOR NOW... BUILDING MORE SOON")