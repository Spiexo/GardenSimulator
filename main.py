import time
import random
from enum import Enum
import json

class Species(Enum):
    VEGETABLES = "Vegetables"
    FRUITS = "Fruits"
    FLOWERS = "Flowers"

class Evolution(Enum):
    SEED = "Seed"
    SHOOT = "Shoot"
    MATURE = "Mature"

class SoilType(Enum):
    CLAY = "Clay"
    SANDY = "Sandy"
    LOAMY = "Loamy"

class Season(Enum):
    SPRING = "Spring"
    SUMMER = "Summer"
    AUTUMN = "Autumn"
    WINTER = "Winter"

class Soil:
    def __init__(self, soil_type: SoilType):
        self.soil_type = soil_type
        self.nutrient_level = 50

    def fertilize(self, amount):
        self.nutrient_level += amount
        self.nutrient_level = min(self.nutrient_level, 100)

    def update_nutrients(self):
        self.nutrient_level -= random.randint(1, 5)
        self.nutrient_level = max(0, self.nutrient_level)

class Garden:
    def __init__(self):
        self.plants = []
        self.lightLevel = random.randint(30, 80)
        self.soil = Soil(SoilType.LOAMY)
        self.season = Season.SPRING
        self.day = 1

    def addPlant(self, plant):
        self.plants.append(plant)

    def removePlant(self, plant):
        self.plants.remove(plant)

    def updateLight(self):
        self.lightLevel = random.randint(30, 80)

    def updateSeason(self):
        if self.day % 90 == 0:
            self.season = Season((self.season.value + 1) % 4)

    def modifPlantsStatus(self):
        for plant in self.plants:
            plant.updateStatus(self.lightLevel, self.soil.nutrient_level, self.season, self.soil.soil_type)

    def information(self):
        for plant in self.plants:
            plant.notifyPlayer()

    def plantStage(self):
        for plant in self.plants:
            if 0 <= plant.maturity <= 33:
                print(f"{plant.name} is a {Evolution.SEED.value}")
            elif 33.01 <= plant.maturity <= 66:
                print(f"{plant.name} is a {Evolution.SHOOT.value}")
            elif 66.01 <= plant.maturity <= 99:
                print(f"{plant.name} is {Evolution.MATURE.value}")
                self.plantProduce()

    def plantProduce(self):
        for plant in self.plants:
            if plant.maturity >= 100:
                if plant.species == Species.VEGETABLES:
                    print(f"Produce {random.randint(4, 10)} {Species.VEGETABLES.value} of {plant.name}")
                elif plant.species == Species.FRUITS:
                    print(f"Produce {random.randint(4, 10)} {Species.FRUITS.value} of {plant.name}")
                elif plant.species == Species.FLOWERS:
                    print(f"Produce {random.randint(2, 6)} {Species.FLOWERS.value} of {plant.name}")

    def triggerEvent(self):
        eventTriggered = False

        if random.random() <= 0.1:
            event = random.choice(["pest", "drought", "storm", "disease", "zombies"])
            if event == "pest":
                print("\n A pest infestation attacks the garden!")
                for plant in self.plants:
                    plant.health -= random.randint(10, 20)
                    plant.health = max(0, plant.health)
            elif event == "drought":
                print("\n A drought hits the garden! Plant water evaporates quickly!")
                for plant in self.plants:
                    plant.water -= random.randint(20, 40)
                    plant.water = max(0, plant.water)
            elif event == "storm":
                print("\n A violent storm hits the garden!")
                for plant in self.plants:
                    plant.health -= random.randint(15, 30)
                    plant.health = max(0, plant.health)
                if self.plants and random.random() < 0.1:
                    removedPlant = random.choice(self.plants)
                    self.removePlant(removedPlant)
                    print(f"❌ {removedPlant.name} was destroyed by the storm!")
            elif event == "disease":
                print("\n A disease spreads through the garden!")
                for plant in self.plants:
                    plant.health -= random.randint(10, 30)
                    plant.health = max(0, plant.health)
            elif event == "zombies" and random.random() <= 0.01:
                print("\n A wave of zombies has trampled your garden!")
                for plant in self.plants:
                    plant.health -= random.randint(30, 70)
                    plant.health = max(0, plant.health)
                if self.plants and random.random() < 0.2:
                    removedPlant = random.choice(self.plants)
                    self.removePlant(removedPlant)
                    print(f"❌ {removedPlant.name} was destroyed by the wave of zombies!")
            eventTriggered = True

        if not eventTriggered:
            print("\n No special events today.")

    def save(self):
        data = {
            "lightLevel": self.lightLevel,
            "soilType": self.soil.soil_type.value,
            "nutrientLevel": self.soil.nutrient_level,
            "season": self.season.value,
            "day": self.day,
            "plants": [
                {
                    "name": plant.name,
                    "water": plant.water,
                    "health": plant.health,
                    "maturity": plant.maturity,
                    "species": plant.species.value,
                    "nutrients": plant.nutrients
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
                self.soil = Soil(SoilType(data["soilType"]))
                self.soil.nutrient_level = data["nutrientLevel"]
                self.season = Season(data["season"])
                self.day = data["day"]
                self.plants = []

                for plantData in data["plants"]:
                    plant = Plants(
                        plantData["name"],
                        plantData["water"],
                        plantData["health"],
                        plantData["maturity"],
                        Species(plantData["species"]),
                        plantData["nutrients"]
                    )
                    self.plants.append(plant)

                print("Successfully loaded!")
        except FileNotFoundError:
            print("No backups found. Starting a new garden.")

class Plants:
    def __init__(self, name, waterRequir, light, growth, species: Species, nutrients=50):
        self.waterNeed = waterRequir
        self.lightNeed = light
        self.growthSpeed = growth
        self.name = name
        self.water = 50
        self.health = 100
        self.maturity = 0
        self.species = species
        self.nutrients = nutrients

    def waterPlant(self, amount):
        self.water += amount
        self.water = max(0, min(self.water, 100))

    def fertilize(self, amount):
        self.nutrients += amount
        self.nutrients = min(self.nutrients, 100)

    def maintain(self):
        self.health += 40
        self.health = min(self.health, 100)

    def updateStatus(self, lightLevel, nutrientLevel, season, soil_type: SoilType):
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

        if nutrientLevel <= 30:
            self.health -= 10
        elif nutrientLevel >= 80:
            self.health -= 5

        if soil_type == SoilType.CLAY:
            growth_multiplier = 0.8
        elif soil_type == SoilType.SANDY:
            growth_multiplier = 0.9
        else:
            growth_multiplier = 1.2

        if self.health > 50 and abs(self.water - self.waterNeed) < 20 and abs(lightLevel - self.lightNeed) < 20 and nutrientLevel > 30:
            self.maturity += self.growthSpeed * growth_multiplier
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
    "3": ("Lettuce", 40, 50, 3, Species.VEGETABLES),
    "4": ("Viool Bergwacht", 40, 40, 20, Species.FLOWERS)
}

myGarden = Garden()

while True:
    print(f"\n🌞 Day {myGarden.day} - Light Level: {myGarden.lightLevel}% - Season: {myGarden.season.value}")
    myGarden.triggerEvent()
    myGarden.information()
    myGarden.plantStage()

    print("\nWhat would you like to do?")
    print("1️⃣  Water a plant")
    print("2️⃣  Fertilize a plant")
    print("3️⃣  Maintain a plant")
    print("4️⃣  Add a plant")
    print("5️⃣  Remove a plant")
    print("6️⃣  Skip to the next day")
    print("7️⃣  Save the game")
    print("8️⃣  Load a save")
    print("9️⃣  Quit")

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
                    amount = int(input("🌱 How much fertilizer to give?: "))
                    plant.fertilize(amount)
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
        myGarden.day += 1
        myGarden.updateLight()
        myGarden.updateSeason()
        myGarden.modifPlantsStatus()

    elif choice == "7":
        myGarden.save()
        print("Save!")

    elif choice == "8":
        myGarden.load()
        print("Game load!")

    elif choice == "9":
        print("👋 Game over. Thanks for playing!")
        break

    else:
        print("❌ Invalid option, try again.")

    time.sleep(0.5)