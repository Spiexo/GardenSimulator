from enums import Species, SoilType
from colorama import Fore, Style

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
        self.garden = None

    def set_garden(self, garden):
        self.garden = garden

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
            self.health -= 40
        elif self.water > self.waterNeed + 20:
            self.health -= 30

        if lightLevel < self.lightNeed - 20:
            self.health -= 20
        elif lightLevel > self.lightNeed + 20:
            self.health -= 10

        if self.nutrients < 30:
            self.health -= 40

        if soilType == SoilType.CLAY:
            growthMultiplier = 0.5
        elif soilType == SoilType.SANDY:
            growthMultiplier = 1
        elif soilType == SoilType.RICHSOIL:
            growthMultiplier = 1.5

        if self.health >= 50 and abs(self.water - self.waterNeed) <= 20 and abs(lightLevel - self.lightNeed) <= 20 and self.nutrients >= 30:
            self.maturity += self.growthSpeed * growthMultiplier
            self.maturity = min(self.maturity, 100)

        if self.health <= 0:
            self.health = 0
            print(f"{Fore.RED}❌ {self.name} has died!{Style.RESET_ALL}")
            if self.garden:
                self.garden.removePlant(self)

    def notifyPlayer(self):
        print(f"\n🌱 {self.name} - Health: {self.health}%, Water: {self.water:.2f}%, Maturity: {self.maturity}%, Soil Nutrients: {self.nutrients}%")
        print(f" {self.name}, which is a {self.species.value}, needs Water: {self.waterNeed}%, Light: {self.lightNeed}%. Its growth speed is {self.growthSpeed}%.")
        if self.health < 50:
            print(f"{Fore.YELLOW}⚠️ {self.name} is in poor health!{Style.RESET_ALL}")
        if self.water < self.waterNeed - 20:
            print(f"{Fore.YELLOW}💧 {self.name} needs water!{Style.RESET_ALL}")
        if self.nutrients < 30:
            print(f"{Fore.YELLOW}⚠️ {self.name} needs nutrients!{Style.RESET_ALL}")