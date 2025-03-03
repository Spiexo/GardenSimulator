from enums import Species
from colorama import Fore, Style

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
            print(f"{Fore.RED}Not enough produce to sell{Style.RESET_ALL}")
            return 0

    def useProduce(self, species: Species, quantity):
        if self.storage[species] >= quantity:
            self.storage[species] -= quantity
            return quantity
        else:
            print(f"{Fore.RED}Not enough produce to use{Style.RESET_ALL}")
            return 0

    def displayInventory(self):
        print(f"{Fore.BLUE}\n📦 Inventory:{Style.RESET_ALL}")
        for species, quantity in self.storage.items():
            print(f"{species.value}: {quantity}")
        print(f"{Fore.GREEN}💰 Money: ${self.money}{Style.RESET_ALL}")