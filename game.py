from colorama import init, Fore, Style
from casino import Casino
from enums import Species
from plants import Plants

init()

availablePlants = {
    "1": ("Tomato", 60, 70, 5, Species.FRUITS),
    "2": ("Carrot", 50, 60, 4, Species.VEGETABLES),
    "3": ("Lettuce", 40, 50, 3, Species.VEGETABLES),
    "4": ("Viool Bergwacht", 40, 40, 20, Species.FLOWERS)
}

def mainLoop(myGarden):
    casino = Casino()
    while True:
        print(f"\n{Fore.YELLOW}🌞 Day {myGarden.day} - Light Level: {myGarden.lightLevel}% - Season: {myGarden.season.value} - Soil Type: {myGarden.soil.soilType.value}{Style.RESET_ALL}")
        
        myGarden.triggerEvent()
        myGarden.information()
        myGarden.plantStage()

        print(f"\n{Fore.CYAN}What would you like to do?{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1.  Water a plant{Style.RESET_ALL}")
        print(f"{Fore.GREEN}2.  Fertilize a plant{Style.RESET_ALL}")
        print(f"{Fore.GREEN}3.  Maintain a plant{Style.RESET_ALL}")
        print(f"{Fore.GREEN}4.  Add a plant{Style.RESET_ALL}")
        print(f"{Fore.GREEN}5.  Remove a plant{Style.RESET_ALL}")
        print(f"{Fore.GREEN}6.  Skip to the next day{Style.RESET_ALL}")
        print(f"{Fore.GREEN}7.  Save the game{Style.RESET_ALL}")
        print(f"{Fore.GREEN}8.  Load a save{Style.RESET_ALL}")
        print(f"{Fore.GREEN}9.  View inventory{Style.RESET_ALL}")
        print(f"{Fore.GREEN}10. Sell produce{Style.RESET_ALL}")
        print(f"{Fore.GREEN}11. Use produce{Style.RESET_ALL}")
        print(f"{Fore.GREEN}12. Visit the Casino{Style.RESET_ALL}")
        print(f"{Fore.GREEN}13. Rules{Style.RESET_ALL}")
        print(f"{Fore.GREEN}14. Quit The Game{Style.RESET_ALL}")

        choice = input(f"{Fore.BLUE}➡️  Your choice: {Style.RESET_ALL}")

        if choice in ["1", "2", "3", "5"] and myGarden.plants:
            print(f"{Fore.CYAN}Select a plant:{Style.RESET_ALL}")
            for i, plant in enumerate(myGarden.plants, 1):
                print(f"{i}. {plant.name}")
            try:
                plantChoice = int(input(f"{Fore.BLUE}➡️  Enter the plant number: {Style.RESET_ALL}")) - 1
                if 0 <= plantChoice < len(myGarden.plants):
                    plant = myGarden.plants[plantChoice]
                    if choice == "1":
                        amount = int(input(f"{Fore.BLUE}💧 How much water to give?: {Style.RESET_ALL}"))
                        plant.waterPlant(amount)
                        print(f"{Fore.GREEN}💧 Watered {plant.name} with {amount} units of water!{Style.RESET_ALL}")
                    elif choice == "2":
                        amount = int(input(f"{Fore.BLUE}🌱 How much fertilizer to add?: {Style.RESET_ALL}"))
                        plant.fertilize(amount)
                        print(f"{Fore.GREEN}🌱 Fertilized {plant.name} with {amount} units of fertilizer!{Style.RESET_ALL}")
                    elif choice == "3":
                        plant.maintain()
                        print(f"{Fore.GREEN}✂️ You maintained {plant.name}!{Style.RESET_ALL}")
                    elif choice == "5":
                        myGarden.removePlant(plant)
                        print(f"{Fore.RED}❌ You removed {plant.name} from the garden.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}❌ Invalid plant.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}❌ Invalid input, please enter a valid number.{Style.RESET_ALL}")

        elif choice == "4":
            print(f"{Fore.CYAN}Select a plant to add:{Style.RESET_ALL}")
            for key, (name, water, light, growth, species) in availablePlants.items():
                print(f"{key}. {name} (Water: {water}, Light: {light}, Growth: {growth})")
            plantChoice = input(f"{Fore.BLUE}➡️  Enter the plant number: {Style.RESET_ALL}")
            if plantChoice in availablePlants:
                name, water, light, growth, species = availablePlants[plantChoice]
                newPlant = Plants(name, water, light, growth, species)
                myGarden.addPlant(newPlant)
                print(f"{Fore.GREEN}🌱 {name} has been added to the garden!{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Invalid choice.{Style.RESET_ALL}")

        elif choice == "6":
            print(f"{Fore.YELLOW}⏭️ Moving to the next day...{Style.RESET_ALL}")
            myGarden.day += 1
            myGarden.updateLight()
            myGarden.updateSeason()
            myGarden.modifPlantsStatus()

        elif choice == "7":
            myGarden.save()
            print(f"{Fore.GREEN}💾 Game saved!{Style.RESET_ALL}")

        elif choice == "8":
            myGarden.load()
            print(f"{Fore.GREEN}💾 Game loaded!{Style.RESET_ALL}")

        elif choice == "9":
            myGarden.inventory.displayInventory()

        elif choice == "10":
            print(f"{Fore.CYAN}Select produce to sell:{Style.RESET_ALL}")
            print(f"1. Vegetables")
            print(f"2. Fruits")
            print(f"3. Flowers")
            sellChoice = input(f"{Fore.BLUE}➡️  Enter the produce number: {Style.RESET_ALL}")
            quantity = int(input(f"{Fore.BLUE}➡️  Enter the quantity to sell: {Style.RESET_ALL}"))

            if sellChoice == "1":
                sold = myGarden.inventory.sellProduce(Species.VEGETABLES, quantity)
                print(f"{Fore.GREEN}💰 Sold {sold} Vegetables!{Style.RESET_ALL}")
            elif sellChoice == "2":
                sold = myGarden.inventory.sellProduce(Species.FRUITS, quantity)
                print(f"{Fore.GREEN}💰 Sold {sold} Fruits!{Style.RESET_ALL}")
            elif sellChoice == "3":
                sold = myGarden.inventory.sellProduce(Species.FLOWERS, quantity)
                print(f"{Fore.GREEN}💰 Sold {sold} Flowers!{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Invalid choice.{Style.RESET_ALL}")

        elif choice == "11":
            print(f"{Fore.CYAN}Select produce to use:{Style.RESET_ALL}")
            print(f"1. Vegetables")
            print(f"2. Fruits")
            print(f"3. Flowers")
            useChoice = input(f"{Fore.BLUE}➡️  Enter the produce number: {Style.RESET_ALL}")
            quantity = int(input(f"{Fore.BLUE}➡️  Enter the quantity to use: {Style.RESET_ALL}"))

            if useChoice == "1":
                used = myGarden.inventory.useProduce(Species.VEGETABLES, quantity)
                print(f"{Fore.GREEN}🍴 Used {used} Vegetables!{Style.RESET_ALL}")
            elif useChoice == "2":
                used = myGarden.inventory.useProduce(Species.FRUITS, quantity)
                print(f"{Fore.GREEN}🍴 Used {used} Fruits!{Style.RESET_ALL}")
            elif useChoice == "3":
                used = myGarden.inventory.useProduce(Species.FLOWERS, quantity)
                print(f"{Fore.GREEN}🍴 Used {used} Flowers!{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Invalid choice.{Style.RESET_ALL}")

        elif choice == "12":
            while True:
                print(f"\n{Fore.YELLOW}🎰 Welcome to the Casino!{Style.RESET_ALL}")
                print(f"{Fore.CYAN}💰 You have ${myGarden.inventory.money}.{Style.RESET_ALL}")
                print(f"1. Play Slot Machine")
                print(f"2. Exit Casino")
                casino_choice = input(f"{Fore.BLUE}➡️  Your choice: {Style.RESET_ALL}")

                if casino_choice == "1":
                    bet = int(input(f"{Fore.BLUE}➡️  How much do you want to bet? ${Style.RESET_ALL}"))
                    if bet > myGarden.inventory.money:
                        print(f"{Fore.RED}❌ You don't have enough money!{Style.RESET_ALL}")
                    else:
                        winnings = casino.playSlotMachine(bet)
                        myGarden.inventory.money += winnings
                        print(f"{Fore.GREEN}💰 Your new balance: ${myGarden.inventory.money}{Style.RESET_ALL}")
                elif casino_choice == "2":
                    print(f"{Fore.YELLOW}👋 Exiting the Casino. Good luck with your garden!{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED}❌ Invalid option, try again.{Style.RESET_ALL}")

        elif choice == "13":
            myGarden.rules()

        elif choice == "14":
            print(f"{Fore.YELLOW}👋 Game over. Thanks for playing!{Style.RESET_ALL}")
            break

        else:
            print(f"{Fore.RED}❌ Invalid option, try again.{Style.RESET_ALL}")