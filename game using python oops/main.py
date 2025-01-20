import time
import random 
import os
import yaml

data ={
    "level":50,
    "experience":400,
    "life":300,
    "defense":50,
    "damage":70,
    "critical":50,
    "penetrating":50,
    "boss_level":14
}

def saveData():
    with open("config.yaml","w")as f:
        yaml.dump(data,f)

def readData():
    global data
    with open("config.yaml", "r") as f:
        data = yaml.safe_load(f)

readData()

class Creator():
    def __init__(self, life, defense, damage):
        self.level = 1
        self.experience = 0
        self.life = life
        self.defense = defense
        self.damage = damage
        self.critical = 10
        self.penetrating = 10
        self.boss_level = 1

                
    def attack(self, user):
        if random.randint(1,100) <= self.critical:
            if random.randint(1,100) <= self.penetrating:
                user.life -= self.damage * 2
            else:
                user.life -=(self.damage - user.defense) * 2
        else:
            if random.randint(1,100) <= self.penetrating:
                user.life -= self.damage
            else:
                user.life -= self.damage - user.defense

def increase_level():
    hero.level += 1
    data["level"] += 1
    saveData()
    print("your level is :", hero.level)
    print("""
          1.life
          2. Defense
          3.Damage
          4. Critical hit chance
          5. Penetrting chance
          """)
    
    choice = int(input("Which one you want to increase?"))
    if choice == 1:
        hero.life += 10
        data["life"] += 10
        saveData()
        print("now you have HP ", hero.life)
        
    elif choice == 2:
        hero.defense += 2
        data["defense"] += 2
        saveData()

        print("now you have defense ", hero.defense)
        
    elif choice == 3:
        hero.damage += 2
        data["damage"] += 2
        saveData()
        print("now you have damage ", hero.damage)
    elif choice == 4:
        hero.critical += 2
        data["critical"] += 2
        saveData()
        print("now you have critical ", hero.critical)
    elif choice == 5:
        hero.penetrating += 2
        data["penetrating"] += 2
        saveData()
        print("now you have penetrating ", hero.penetrating)
    else:
        pass

hero = Creator(data["life"],data["defense"],data["damage"])
hero.level = data["level"]
hero.experience = data["experience"]
hero.boss_level = data["boss_level"]
hero.critical = data["critical"]
hero.penetrating = data["penetrating"]

creature = Creator(40,10,20)
        
def attack_creature():
    creature_no = int(input("How many cretures do you wanna fight?\n"))
    no_exp = creature_no
    hero_life = hero.life
    
    version = int(input("""
        1. Show the details
        2. Don't show details                        
                        """))
    if version == 1:
        while True:
            input("PRESS ENTER TO CONTINUE")
            time.sleep(2)
            hero.attack(creature)
            
            if creature.life <= 0 and creature_no==1:
                print("Creature is dead YOU WIN")
                hero.experience += no_exp*50
                data["experience"] += no_exp*50
                saveData()
                hero.life = hero_life
                
                if hero.experience >= hero.level*100:
                    increase_level()
                    hero.experience= 0
                    data["experience"] = 0
                    saveData()
                break
            
            elif creature.life <= 0 and creature_no>1:
                creature_no -=1
                print("Creature has killed 1 creature ", creature.life)
                creature.life = 40
        
            print("Now creature has ", creature.life)
            time.sleep(2)
            print("Now creature are attacking you")
            time.sleep(2)
            for creatures in range(creature_no):
                creature.attack(hero)
            if hero.life <= 0:
                print("You are dead u lost")
                break
            print("you have ", hero.life)
    
    elif version == 2:
        while True:
            hero.attack(creature)
            if creature.life <= 0 and creature_no==1:
                print("Creature is dead YOU WIN")
                hero.experience += no_exp*50
                data["experience"] += no_exp*50
                saveData()
                hero.life = hero_life
                
                if hero.experience >= hero.level*100:
                    increase_level()
                    hero.experience= 0
                    data["experience"] = 0
                    saveData()
                break

            elif creature.life <= 0 and creature_no>1:
                creature_no -=1
                creature.life = 40
            for creatures in range(creature_no):
                creature.attack(hero)
                
            print("you have HP left ", hero.life)
            if hero.life <= 0:
                print("You are dead u lost")
                break    


def attack_boss():
    boss = Creator(100+ 10* hero.boss_level,20+2*hero.boss_level,35+3*hero.boss_level)
    hero_life = hero.life
    
    version = int(input("""
        1. Show the details
        2. Don't show details                        
                        """))
    if version == 1:
        while True: 
            input("PRESS ENTER TO CONTINUE")
            time.sleep(2)
            hero.attack(boss)
            
            if boss.life <= 0:
                print("BOSS is dead YOU WIN")
                
                hero.life = hero_life
                hero.boss_level += 1
                data["boss_level"] += 1
                saveData()
                break
            
            print("Now BOSS has ", boss.life)
            time.sleep(2)
            print("Now BOSS are attacking you")
            time.sleep(2)
            boss.attack(hero)
            if hero.life <= 0:
                print("You are dead u lost")
                break
            print("you have ", hero.life)
    
    elif version == 2:
        while True: 
            hero.attack(boss)
            if boss.life <= 0:
                print("BOSS is dead YOU WIN")
                hero.life = hero_life
                hero.boss_level += 1
                data["boss_level"] += 1
                saveData()
                break
            print("Now BOSS has ", boss.life)
            boss.attack(hero)
            if hero.life <= 0:
                print("You are dead u lost")
                break
            print("you have ", hero.life)  
    
    if hero.boss_level > 100:
        print("GAME OVER")
          
def show(h):
    print(f"""
          1. life : {h.life}
          2. defense : {h.defense}
          3. damage : {h.damage}
          4. critical hit : {h.critical}
          5. pentration : {h.penetrating}
          """)

def main():
    while True:
        print("""
    1. Attack Creature
    2. Attack BOSS
    3. EXIT
    """)
        choice = int(input("Choose Your Option\n"))
        os.system('cls' if os.name == 'nt' else 'clear')
        if choice == 1:
            attack_creature()
        elif choice == 2:
            attack_boss()
        elif choice == 3:
            break


main()