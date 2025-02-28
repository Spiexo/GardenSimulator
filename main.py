import time
import random
from enum import Enum
import json

class Garden:
    def __init__(self):
        self.plants = []
        self.lightLevel = random.randint(30, 80)

    def addPlant(self, plant):
        self.plants.append(plant)

    def removePlant(self, plant):
        self.plants.remove(plant)

    def updateLight(self):
        self.lightLevel = random.randint(30, 80)

    def modifPlantsStatus(self):
        for plant in self.plants:
            plant.updateStatus(self.lightLevel)

    def information(self):
        for plant in self.plants:
            plant.notifyPlayer()

    def plantStage(self) :
        for plant in self.plants:
            if 0 <= plant.maturity <= 33 :
                print(f"{plant.name} is a seed")
            if 33.01 <= plant.maturity <= 66 :
                print(f"{plant.name} is a shoot ")
            if 66.01 <= plant.maturity <= 99 :
                print(f"{plant.name} is mature")
                plant.plantProduce()

#A modifier pour la production en fonction des especes
    # def plantProduce(self) :
    #     for plant in self.plants:
    #         if plant.specie :
    #             pass
    #         pass

    def triggerEvent(self, day):
        eventTriggered = False
        
        if 2 <= day <= 4 and random.random() <= 0.3:
            print("\n A pest infestation attacks the garden!")
            for plant in self.plants:
                plant.health -= random.randint(10, 20)
                plant.health = max(0, plant.health)
            eventTriggered = True

        if 5 <= day <= 7 and random.random() <= 0.4:
            print("\n A heatwave hits the garden! Plant water evaporates quickly!")
            for plant in self.plants:
                plant.water -= random.randint(20, 40)
                plant.water = max(0, plant.water)
            eventTriggered = True

        if 2 <= day and random.random() <= 0.05:
            print("\n A violent storm hits the garden!")
            for plant in self.plants:
                plant.health -= random.randint(15, 30)
                plant.health = max(0, plant.health)
            if self.plants and random.random() < 0.1:
                removedPlant = random.choice(self.plants)
                self.removePlant(removedPlant)
                print(f"❌ {removedPlant.name} was destroyed by the storm!")
            eventTriggered = True

        if not eventTriggered:
            print("\n No special events today.")

    def save(self):
        data = {
            "lightLevel": self.lightLevel,
            "plants": [
                {
                    "name": plant.name,
                    "water": plant.water,
                    "health": plant.health,
                    "maturity": plant.maturity,
                    "species": plant.species.value
                }
                for plant in self.plants
            ]
        }
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load(self):
        try:
            with open("data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                
                self.lightLevel = data["lightLevel"]
                self.plants = []
                
                for plant_data in data["plants"]:
                    plant = Plants(
                        plant_data["name"],
                        plant_data["water"],
                        plant_data["health"],
                        plant_data["maturity"],
                        Species(plant_data["species"])
                    )
                    self.plants.append(plant)
                    
                print("✔ Partie chargée avec succès !")
        
        except FileNotFoundError:
            print("Aucune sauvegarde trouvée. Démarrage d'un nouveau jardin.")


myGarden = Garden()

class Species(Enum):
    VEGETABLES = "Vegetables"
    FRUITS = "Fruits"
    FLOWER = "Flower"


class Plants:
    def __init__(self, name, waterRequir, light, growth, species: Species):
        self.waterNeed = waterRequir
        self.lightNeed = light
        self.growthSpeed = growth
        self.name = name
        self.water = 50
        self.health = 100
        self.maturity = 0
        self.species = species

    def waterPlant(self, amount):
        self.water += amount
        self.water = max(0, min(self.water, 100))

    def fertilize(self):
        self.maturity += self.growthSpeed * 2
        self.maturity = min(self.maturity, 100)

    def maintain(self):
        self.health += 40
        self.health = min(self.health, 100)

    def updateStatus(self, lightLevel):
        evaporationRate = lightLevel * 0.05
        self.water -= evaporationRate
        self.water = max(0, self.water)

        if self.water <= self.waterNeed - 20:
            self.health -= 10
        elif self.water >= self.waterNeed + 20:
            self.health -= 5

        if lightLevel <= self.lightNeed - 20:
            self.health -= 10
        elif lightLevel >= self.lightNeed + 20:
            self.health -= 5

        if self.health > 50 and abs(self.water - self.waterNeed) < 20 and abs(lightLevel - self.lightNeed) < 20:
            self.maturity += self.growthSpeed
            self.maturity = min(self.maturity, 100)

        if self.health <= 0:
            self.health = 0
            print(f"❌ {self.name} has died!")
            myGarden.removePlant(self)

    def notifyPlayer(self):
        print(f"\n🌱 {self.name} - Health: {self.health}%, Water: {self.water:.2f}%, Maturity: {self.maturity}%")
        print(f" {self.name}, which is a {self.species.value}, needs Water: {self.waterNeed}%, Light: {self.lightNeed}%. Its growth speed is {self.growthSpeed}%.")

        if self.health <= 50:
            print(f"⚠️ {self.name} is in poor health!")
        if self.water <= self.waterNeed - 20:
            print(f"💧 {self.name} needs water!")
        if self.maturity >= 100:
            print(f"🎉 {self.name} is fully matured!")

availablePlants = {
    "1": ("Tomato", 60, 70, 5, Species.FRUITS),
    "2": ("Carrot", 50, 60, 4, Species.VEGETABLES),
    "3": ("Lettuce", 40, 50, 3, Species.VEGETABLES)
}

day = 1

while True:
    print(f"\n🌞 Day {day} - Light Level: {myGarden.lightLevel}%")
    myGarden.triggerEvent(day)
    myGarden.information()
    myGarden.plantStage()

    print("\nWhat would you like to do?")
    print("1️⃣  Water a plant")
    print("2️⃣  Fertilize a plant")
    print("3️⃣  Maintain a plant")
    print("4️⃣  Add a plant")
    print("5️⃣  Remove a plant")
    print("6  Skip to the next day")
    print("7  Save the game")
    print("8  Load a save")
    print("9  Quit")

    choice = input("➡️  Your choice: ")

    if choice in ["1", "2", "3", "5"] and myGarden.plants:
        print("Select a plant:")
        for i, plant in enumerate(myGarden.plants, 1):
            print(f"{i}. {plant.name}")
        try:
            plantChoice = int(input("➡️  Enter the plant number: ")) - 1
            if 0 <= plantChoice < len(myGarden.plants):
                plant = myGarden.plants[plantChoice]
                if choice == "1":
                    amount = int(input("💧 How much water to give?: "))
                    plant.waterPlant(amount)
                elif choice == "2":
                    plant.fertilize()
                    print(f"🌱 You fertilized {plant.name}!")
                elif choice == "3":
                    plant.maintain()
                    print(f"✂️ You maintained {plant.name}!")
                elif choice == "5":
                    myGarden.removePlant(plant)
                    print(f"❌ You removed {plant.name} from the garden.")
            else:
                print("❌ Invalid plant.")
        except ValueError:
            print("❌ Invalid input, please enter a valid number.")

    elif choice == "4":
        print("Select a plant to add:")
        for key, (name, water, light, growth, species) in availablePlants.items():
            print(f"{key}. {name} (Water: {water}, Light: {light}, Growth: {growth})")
        plantChoice = input("➡️  Enter the plant number: ")
        if plantChoice in availablePlants:
            name, water, light, growth, species = availablePlants[plantChoice]
            newPlant = Plants(name, water, light, growth, species)
            myGarden.addPlant(newPlant)
            print(f"🌱 {name} has been added to the garden!")
        else:
            print("❌ Invalid choice.")

    elif choice == "6":
        print("⏭️ Moving to the next day...")
        day += 1
        myGarden.updateLight()
        myGarden.modifPlantsStatus()

    elif choice == "7":
        print("Save!")
        myGarden.save()
        print("Come back soon")
        break

    elif choice == "8":
        myGarden.load()
        print("Game load!")

    elif choice == "9":
        print("👋 Game over. Thanks for playing!")
        break

    else:
        print("❌ Invalid option, try again.")

    time.sleep(0.5)
