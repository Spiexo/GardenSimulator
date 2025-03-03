import random
import json
from colorama import Fore, Style
from enums import SoilType, Season, Species, Evolution
from inventory import Inventory
from plants import Plants

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
        print(f"{Fore.BLUE}\n📜 Welcome to Garden Simulator! Here are the rules:{Style.RESET_ALL}")
        print(f"1. You start with a garden and can choose the type of soil ({Fore.GREEN}EASY{Style.RESET_ALL}, {Fore.YELLOW}NORMAL{Style.RESET_ALL}, {Fore.RED}HARD{Style.RESET_ALL}).")
        print("2. Each day, you can water, fertilize, or maintain your plants.")
        print("3. Plants grow over time and produce vegetables, fruits, or flowers.")
        print("4. You can sell or use the produce to gamble all your money.")
        print("5. Random events like pests, droughts, storms, diseases, or even zombies can occur.")
        print("6. Your goal is to keep your plants healthy and maximize your harvest.")
        print("7. The game ends when you decide to quit. Have fun!\n")

    def difficulty(self):
        print(f"{Fore.BLUE}Select your soil:{Style.RESET_ALL}")
        print(f"1. Rich soil {Fore.GREEN}(EASY){Style.RESET_ALL}")
        print(f"2. Sandy {Fore.YELLOW}(NORMAL){Style.RESET_ALL}")
        print(f"3. Clay {Fore.RED}(HARD){Style.RESET_ALL}")
        soilChoice = input(f"{Fore.BLUE}➡️  Enter the soil number: {Style.RESET_ALL}")

        if soilChoice == "1":
            self.soil = Soil(SoilType.RICHSOIL)
        elif soilChoice == "2":
            self.soil = Soil(SoilType.SANDY)
        elif soilChoice == "3":
            self.soil = Soil(SoilType.CLAY)
        else:
            print(f"{Fore.RED}❌ Invalid choice. Defaulting to Rich soil (EASY).{Style.RESET_ALL}")
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
                print(f"{Fore.YELLOW}{plant.name} is a {Evolution.SEED.value}{Style.RESET_ALL}")
            elif 33.01 <= plant.maturity <= 66:
                print(f"{Fore.YELLOW}{plant.name} is a {Evolution.SHOOT.value}{Style.RESET_ALL}")
            elif 66.01 <= plant.maturity <= 99:
                print(f"{Fore.YELLOW}{plant.name} is {Evolution.MATURE.value}{Style.RESET_ALL}")
            elif plant.maturity >= 100:
                print(f"{Fore.GREEN}{plant.name} is fully matured and ready to produce!{Style.RESET_ALL}")
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
                    print(f"{Fore.YELLOW}🌱 {plant.name} produced {production} {Species.VEGETABLES.value}!{Style.RESET_ALL}")
                elif plant.species == Species.FRUITS:
                    production = int(random.randint(4, 10) * productionMultiplier)
                    self.inventory.addProduce(Species.FRUITS, production)
                    print(f"{Fore.YELLOW}🌱 {plant.name} produced {production} {Species.FRUITS.value}!{Style.RESET_ALL}")
                elif plant.species == Species.FLOWERS:
                    production = int(random.randint(2, 6) * productionMultiplier)
                    self.inventory.addProduce(Species.FLOWERS, production)
                    print(f"{Fore.YELLOW}🌱 {plant.name} produced {production} {Species.FLOWERS.value}!{Style.RESET_ALL}")

                plant.nutrients -= 60
                plant.nutrients = max(0, plant.nutrients)

    def triggerEvent(self):
        eventTriggered = False
        if self.day > 1 and random.random() <= 0.1:
            event = random.choice(["pest", "drought", "storm", "disease", "zombies"])

            if event == "pest":
                eventTriggered = True
                print(f"{Fore.YELLOW}\n A pest infestation attacks the garden!{Style.RESET_ALL}")
                for plant in self.plants:
                    plant.health -= random.randint(10, 20)
                    plant.health = max(0, plant.health)

            elif event == "drought":
                eventTriggered = True
                print(f"{Fore.YELLOW}\n A drought hits the garden! Plant water evaporates quickly!{Style.RESET_ALL}")
                for plant in self.plants:
                    plant.water -= random.randint(20, 40)
                    plant.water = max(0, plant.water)

            elif event == "storm":
                eventTriggered = True
                print(f"{Fore.YELLOW}\n A violent storm hits the garden!{Style.RESET_ALL}")
                for plant in self.plants:
                    plant.health -= random.randint(15, 30)
                    plant.health = max(0, plant.health)
                if self.plants and random.random() < 0.1:
                    removedPlant = random.choice(self.plants)
                    self.removePlant(removedPlant)
                    print(f"{Fore.RED}❌ {removedPlant.name} was destroyed by the storm!{Style.RESET_ALL}")

            elif event == "disease":
                eventTriggered = True
                print(f"{Fore.YELLOW}\n A disease spreads through the garden!{Style.RESET_ALL}")
                for plant in self.plants:
                    plant.health -= random.randint(10, 30)
                    plant.health = max(0, plant.health)

            elif event == "zombies" and random.random() <= 0.05:
                eventTriggered = True
                print(f"{Fore.YELLOW}\n A wave of zombies has trampled your garden!{Style.RESET_ALL}")
                for plant in self.plants:
                    plant.health -= random.randint(30, 70)
                    plant.health = max(0, plant.health)
                if self.plants and random.random() < 0.2:
                    removedPlant = random.choice(self.plants)
                    self.removePlant(removedPlant)
                    print(f"{Fore.RED}❌ {removedPlant.name} was destroyed by the wave of zombies!{Style.RESET_ALL}")

            if not eventTriggered:
                self.event = None
                print(f"{Fore.YELLOW}\n No special events today.{Style.RESET_ALL}")

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
                print(f"{Fore.GREEN}Successfully Saved!{Style.RESET_ALL}")

        except FileNotFoundError:
            print(f"{Fore.RED}Error saving garden.{Style.RESET_ALL}")

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

                print(f"{Fore.GREEN}Successfully loaded!{Style.RESET_ALL}")
        except FileNotFoundError:
            print(f"{Fore.RED}No backups found.{Style.RESET_ALL}")
