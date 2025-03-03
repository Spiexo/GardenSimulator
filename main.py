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
    RICHSOIL = "Richsoil"

class Season(Enum):
    SPRING = "Spring"
    SUMMER = "Summer"
    AUTUMN = "Autumn"
    WINTER = "Winter"

class Inventory:
    def __init__(self):
        self.storage = {
            Species.VEGETABLES: 0,
            Species.FRUITS: 0,
            Species.FLOWERS: 0
        }
        self.money = 99999

    def addProduce(self, species: Species, quantity):
        self.storage[species] += quantity

    def sellProduce(self, species: Species, quantity):
        if self.storage[species] >= quantity:
            self.storage[species] -= quantity
            if species == Species.VEGETABLES:
                self.money += quantity * 5
            elif species == Species.FRUITS:
                self.money += quantity * 10
            elif species == Species.FLOWERS:
                self.money += quantity * 15
            return quantity
        else:
            print("Not enough produce to sell")
            return 0

    def useProduce(self, species: Species, quantity):
        if self.storage[species] >= quantity:
            self.storage[species] -= quantity
            return quantity
        else:
            print("Not enough produce to use")
            return 0

    def displayInventory(self):
        print("\n📦 Inventory:")
        for species, quantity in self.storage.items():
            print(f"{species.value}: {quantity}")
        print(f"💰 Money: ${self.money}")

class Soil:
    def __init__(self, soilType: SoilType):
        self.soilType = soilType

class Garden:
    def __init__(self):
        self.plants = []
        self.lightLevel = random.randint(30, 80)
        self.soil = Soil(SoilType.RICHSOIL)
        self.season = Season.SPRING
        self.day = 1
        self.inventory = Inventory()
        self.event = None

    def rules(self):
        print("\n📜 Welcome to Garden Simulator! Here are the rules:")
        print("1. You start with a garden and can choose the type of soil (EASY, NORMAL, HARD).")
        print("2. Each day, you can water, fertilize, or maintain your plants.")
        print("3. Plants grow over time and produce vegetables, fruits, or flowers.")
        print("4. You can sell or use the produce to earn points or improve your garden.")
        print("5. Random events like pests, droughts, storms, diseases, or even zombies can occur.")
        print("6. Your goal is to keep your plants healthy and maximize your harvest.")
        print("7. The game ends when you decide to quit. Have fun!\n")

    def difficulty(self):
        print("Select your soil:")
        print("1. Rich soil (EASY)")
        print("2. Sandy (NORMAL)")
        print("3. Clay (HARD)")
        soilChoice = input("➡️  Enter the soil number: ")

        if soilChoice == "1":
            self.soil = Soil(SoilType.RICHSOIL)
            print("You chose Rich soil (EASY)!")
        elif soilChoice == "2":
            self.soil = Soil(SoilType.SANDY)
            print("You chose Sandy (NORMAL)!")
        elif soilChoice == "3":
            self.soil = Soil(SoilType.CLAY)
            print("You chose Clay (HARD)!")
        else:
            print("❌ Invalid choice. Defaulting to Rich soil (EASY).")
            self.soil = Soil(SoilType.RICHSOIL)

    def addPlant(self, plant):
        self.plants.append(plant)

    def removePlant(self, plant):
        self.plants.remove(plant)

    def updateLight(self):
        self.lightLevel = random.randint(30, 80)

    def updateSeason(self):
        if self.day % 90 == 0:
            seasons = list(Season)
            self.season = seasons[(seasons.index(self.season) + 1) % len(seasons)]

    def modifPlantsStatus(self):
        for plant in self.plants:
            plant.updateStatus(self.lightLevel, self.soil.soilType)

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
            elif plant.maturity >= 100:
                print(f"{plant.name} is fully matured and ready to produce!")
                self.plantProduce()

    def plantProduce(self):
        for plant in self.plants:
            if plant.maturity >= 100:
                if plant.nutrients < 30:
                    productionMultiplier = 0.5
                elif 30 <= plant.nutrients <= 80:
                    productionMultiplier = 1.0
                elif 80 < plant.nutrients:
                    productionMultiplier = 1.5

                if plant.species == Species.VEGETABLES:
                    production = int(random.randint(4, 10) * productionMultiplier)
                    self.inventory.addProduce(Species.VEGETABLES, production)
                    print(f"🌱 {plant.name} produced {production} {Species.VEGETABLES.value}!")
                elif plant.species == Species.FRUITS:
                    production = int(random.randint(4, 10) * productionMultiplier)
                    self.inventory.addProduce(Species.FRUITS, production)
                    print(f"🌱 {plant.name} produced {production} {Species.FRUITS.value}!")
                elif plant.species == Species.FLOWERS:
                    production = int(random.randint(2, 6) * productionMultiplier)
                    self.inventory.addProduce(Species.FLOWERS, production)
                    print(f"🌱 {plant.name} produced {production} {Species.FLOWERS.value}!")

                plant.nutrients -= 60
                plant.nutrients = max(0, plant.nutrients)

    def triggerEvent(self):
        eventTriggered = False
        if random.random() <= 0.1:
            event = random.choice(["pest", "drought", "storm", "disease", "zombies"])

            if event == "pest":
                eventTriggered = True
                print("\n A pest infestation attacks the garden!")
                for plant in self.plants:
                    plant.health -= random.randint(10, 20)
                    plant.health = max(0, plant.health)

            elif event == "drought":
                eventTriggered = True
                print("\n A drought hits the garden! Plant water evaporates quickly!")
                for plant in self.plants:
                    plant.water -= random.randint(20, 40)
                    plant.water = max(0, plant.water)

            elif event == "storm":
                eventTriggered = True
                print("\n A violent storm hits the garden!")
                for plant in self.plants:
                    plant.health -= random.randint(15, 30)
                    plant.health = max(0, plant.health)
                if self.plants and random.random() < 0.1:
                    removedPlant = random.choice(self.plants)
                    self.removePlant(removedPlant)
                    print(f"❌ {removedPlant.name} was destroyed by the storm!")

            elif event == "disease":
                eventTriggered = True
                print("\n A disease spreads through the garden!")
                for plant in self.plants:
                    plant.health -= random.randint(10, 30)
                    plant.health = max(0, plant.health)

            elif event == "zombies" and random.random() <= 0.05:
                eventTriggered = True
                print("\n A wave of zombies has trampled your garden!")
                for plant in self.plants:
                    plant.health -= random.randint(30, 70)
                    plant.health = max(0, plant.health)
                if self.plants and random.random() < 0.2:
                    removedPlant = random.choice(self.plants)
                    self.removePlant(removedPlant)
                    print(f"❌ {removedPlant.name} was destroyed by the wave of zombies!")

            if not eventTriggered:
                self.event = None
                print("\n No special events today.")

    def save(self):
        try:
            data = {
                "lightLevel": self.lightLevel,
                "soilType": self.soil.soilType.value,
                "nutrientLevel": self.soil.nutrientLevel,
                "season": self.season.value,
                "day": self.day,
                "event": self.event,
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
                ],
                "inventory": {
                    "vegetables": self.inventory.storage[Species.VEGETABLES],
                    "fruits": self.inventory.storage[Species.FRUITS],
                    "flowers": self.inventory.storage[Species.FLOWERS],
                    "money": self.inventory.money
                }
            }
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                print("Successfully Saved!")

        except FileNotFoundError:
            print("Error saving garden.")

    def load(self):
        try:
            with open("data.json", "r", encoding="utf-8") as f:
                data = json.load(f)

                self.lightLevel = data["lightLevel"]
                self.soil = Soil(SoilType(data["soilType"]))
                self.soil.nutrientLevel = data["nutrientLevel"]
                self.season = Season(data["season"])
                self.day = data["day"]
                self.event = data["event"]
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

                self.inventory.storage[Species.VEGETABLES] = data["inventory"]["vegetables"]
                self.inventory.storage[Species.FRUITS] = data["inventory"]["fruits"]
                self.inventory.storage[Species.FLOWERS] = data["inventory"]["flowers"]
                self.inventory.money = data["inventory"]["money"]

                print("Successfully loaded!")
        except FileNotFoundError:
            print("No backups found.")

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

    def updateStatus(self, lightLevel, soilType: SoilType):
        evaporationRate = lightLevel * 0.05
        self.water -= evaporationRate
        self.water = max(0, self.water)

        if self.water < self.waterNeed - 20:
            self.health -= 10
        elif self.water > self.waterNeed + 20:
            self.health -= 5

        if lightLevel < self.lightNeed - 20:
            self.health -= 10
        elif lightLevel > self.lightNeed + 20:
            self.health -= 5

        if self.nutrients < 30:
            self.health -= 10
        elif self.nutrients > 80:
            self.health -= 5

        if soilType == SoilType.CLAY:
            growth_multiplier = 0.8
        elif soilType == SoilType.SANDY:
            growth_multiplier = 0.9
        elif soilType == SoilType.RICHSOIL:
            growth_multiplier = 1.2

        if self.health >= 50 and abs(self.water - self.waterNeed) <= 20 and abs(lightLevel - self.lightNeed) <= 20 and self.nutrients >= 30:
            self.maturity += self.growthSpeed * growth_multiplier
            self.maturity = min(self.maturity, 100)

        if self.health <= 0:
            self.health = 0
            print(f"❌ {self.name} has died!")
            myGarden.removePlant(self)

    def notifyPlayer(self):
        print(f"\n🌱 {self.name} - Health: {self.health}%, Water: {self.water:.2f}%, Maturity: {self.maturity}%, Soil Nutrients: {self.nutrients}%")
        print(f" {self.name}, which is a {self.species.value}, needs Water: {self.waterNeed}%, Light: {self.lightNeed}%. Its growth speed is {self.growthSpeed}%.")
        if self.health < 50:
            print(f"⚠️ {self.name} is in poor health!")
        if self.water < self.waterNeed - 20:
            print(f"💧 {self.name} needs water!")
        if self.nutrients < 30:
            print(f"⚠️ {self.nutrients} needs nutrients!")
        if self.maturity == 100:
            print(f"🎉 {self.name} is fully matured!")

availablePlants = {
    "1": ("Tomato", 60, 70, 5, Species.FRUITS),
    "2": ("Carrot", 50, 60, 4, Species.VEGETABLES),
    "3": ("Lettuce", 40, 50, 3, Species.VEGETABLES),
    "4": ("Viool Bergwacht", 40, 40, 20, Species.FLOWERS)
}

class Casino:
    def __init__(self):
        self.symbols = ["🍒", "🍋", "🍇", "🍉", "🔔", "💎"]

    def playSlotMachine(self, bet):

        result = [random.choice(self.symbols) for _ in range(3)]
        print("🎰 Slot Machine Result:", " ".join(result))

        if result[0] == result[1] == result[2]:
            winnings = bet * 10
            print(f"🎉 Jackpot! You won ${winnings}!")
        elif result[0] == result[1] or result[1] == result[2] or result[0] == result[2]:
            winnings = bet * 2
            print(f"🎉 You won ${winnings}!")
        else:
            winnings = -bet
            print(f"😢 You lost ${bet}.")

        return winnings

def mainLoop(myGarden):
    
    while True:
        print(f"\n🌞 Day {myGarden.day} - Light Level: {myGarden.lightLevel}% - Season: {myGarden.season.value} - Soil Type: {myGarden.soil.soilType.value}")
        myGarden.triggerEvent()
        myGarden.information()
        myGarden.plantStage()

        print("\nWhat would you like to do?")
        print("1.  Water a plant")
        print("2.  Fertilize a plant")
        print("3.  Maintain a plant")
        print("4.  Add a plant")
        print("5.  Remove a plant")
        print("6.  Skip to the next day")
        print("7.  Save the game")
        print("8.  Load a save")
        print("9.  View inventory")
        print("10. Sell produce")
        print("11. Use produce")
        print("12. Visit the Casino")
        print("13. Quit The Game")

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
                        amount = int(input("🌱 How much fertilizer to add?: "))
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

        elif choice == "8":
            myGarden.load()

        elif choice == "9":
            myGarden.inventory.displayInventory()

        elif choice == "10":
            print("Select produce to sell:")
            print("1. Vegetables")
            print("2. Fruits")
            print("3. Flowers")
            sellChoice = input("➡️  Enter the produce number: ")
            quantity = int(input("➡️  Enter the quantity to sell: "))

            if sellChoice == "1":
                sold = myGarden.inventory.sellProduce(Species.VEGETABLES, quantity)
                print(f"💰 Sold {sold} Vegetables!")
            elif sellChoice == "2":
                sold = myGarden.inventory.sellProduce(Species.FRUITS, quantity)
                print(f"💰 Sold {sold} Fruits!")
            elif sellChoice == "3":
                sold = myGarden.inventory.sellProduce(Species.FLOWERS, quantity)
                print(f"💰 Sold {sold} Flowers!")
            else:
                print("❌ Invalid choice.")

        elif choice == "11":
            print("Select produce to use:")
            print("1. Vegetables")
            print("2. Fruits")
            print("3. Flowers")
            useChoice = input("➡️  Enter the produce number: ")
            quantity = int(input("➡️  Enter the quantity to use: "))

            if useChoice == "1":
                used = myGarden.inventory.useProduce(Species.VEGETABLES, quantity)
                print(f"🍴 Used {used} Vegetables!")
            elif useChoice == "2":
                used = myGarden.inventory.useProduce(Species.FRUITS, quantity)
                print(f"🍴 Used {used} Fruits!")
            elif useChoice == "3":
                used = myGarden.inventory.useProduce(Species.FLOWERS, quantity)
                print(f"🍴 Used {used} Flowers!")
            else:
                print("❌ Invalid choice.")

        elif choice == "12":
            while True:
                print("\n🎰 Welcome to the Casino!")
                print(f"💰 You have ${myGarden.inventory.money}.")
                print("1. Play Slot Machine")
                print("2. Exit Casino")
                casino_choice = input("➡️  Your choice: ")

                if casino_choice == "1":
                    bet = int(input("➡️  How much do you want to bet? $"))
                    if bet > myGarden.inventory.money:
                        print("❌ You don't have enough money!")
                    else:
                        winnings = casino.playSlotMachine(bet)
                        myGarden.inventory.money += winnings
                        print(f"💰 Your new balance: ${myGarden.inventory.money}")
                elif casino_choice == "2":
                    print("👋 Exiting the Casino. Good luck with your garden!")
                    break
                else:
                    print("❌ Invalid option, try again.")
        elif choice == "13":
            print("👋 Game over. Thanks for playing!")
            break

        else:
            print("❌ Invalid option, try again.")

        time.sleep(0.5)

casino = Casino()
myGarden = Garden()
myGarden.difficulty()
mainLoop(myGarden)