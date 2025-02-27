import time
import random

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
                plant.plantPruce()
#A modifier pour la production en fonction des especes
    # def plantProduce(self) :
    #     for plant in self.plants:
    #         if plant.specie :
    #             pass
    #         pass

    def triggerEvent(self, day):
        event_triggered = False
        
        if 2 <= day <= 4 and random.random() <= 0.3:
            print("\n A pest infestation attacks the garden!")
            for plant in self.plants:
                plant.health -= random.randint(10, 20)
                plant.health = max(0, plant.health)
            event_triggered = True

        if 5 <= day <= 7 and random.random() <= 0.4:
            print("\n A heatwave hits the garden! Plant water evaporates quickly!")
            for plant in self.plants:
                plant.water -= random.randint(20, 40)
                plant.water = max(0, plant.water)
            event_triggered = True

        if 2 <= day and random.random() <= 0.05:
            print("\n A violent storm hits the garden!")
            for plant in self.plants:
                plant.health -= random.randint(15, 30)
                plant.health = max(0, plant.health)
            if self.plants and random.random() < 0.1:
                removed_plant = random.choice(self.plants)
                self.removePlant(removed_plant)
                print(f"❌ {removed_plant.name} was destroyed by the storm!")
            event_triggered = True

        if not event_triggered:
            print("\n No special events today.")

my_garden = Garden()

class Plants:
    def __init__(self, name, waterRequir, light, growth, species):
        self.waterNeed = waterRequir
        self.lightNeed = light
        self.growthSpeed = growth
        self.name = name
        self.water = 50
        self.health = 100
        self.maturity = 0
        self.specie = species

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
        evaporation_rate = lightLevel * 0.05
        self.water -= evaporation_rate
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
            my_garden.removePlant(self)

    def notifyPlayer(self):
        print(f"\n🌱 {self.name} - Health: {self.health}%, Water: {self.water:.2f}%, Maturity: {self.maturity}%")
        print(f" {self.name} needs Water: {self.waterNeed}%, Light: {self.lightNeed}%. Possede Growth: {self.growthSpeed}%")
        if self.health <= 50:
            print(f"⚠️ {self.name} is in poor health!")
        if self.water <= self.waterNeed - 20:
            print(f"💧 {self.name} needs water!")
        if self.maturity >= 100:
            print(f"🎉 {self.name} is fully matured!")


# class Vegetables(Plants):
#     def __init__(self, name, waterRequir, light, growth):
#         super().__init__(name, waterRequir, light, growth)

# class Fruits(Plants):
#     def __init__(self, name, waterRequir, light, growth):
#         super().__init__(name, waterRequir, light, growth)

# class Flower(Plants):
#     def __init__(self, name, waterRequir, light, growth):
#         super().__init__(name, waterRequir, light, growth)



available_plants = {
    "1": ("Tomato", 60, 70, 5, "fe"),
    "2": ("Carrot", 50, 60, 4, "fe"),
    "3": ("Lettuce", 40, 50, 3, "fe")
}

day = 1

while True:
    print(f"\n🌞 Day {day} - Light Level: {my_garden.lightLevel}%")
    my_garden.plantStage()
    my_garden.triggerEvent(day)
    my_garden.information()

    print("\nWhat would you like to do?")
    print("1️⃣  Water a plant")
    print("2️⃣  Fertilize a plant")
    print("3️⃣  Maintain a plant")
    print("4️⃣  Add a plant")
    print("5️⃣  Remove a plant")
    print("6  Skip to the next day")
    print("7  Quit")

    choice = input("➡️  Your choice: ")

    if choice in ["1", "2", "3", "5"] and my_garden.plants:
        print("Select a plant:")
        for i, plant in enumerate(my_garden.plants, 1):
            print(f"{i}. {plant.name}")
        try:
            plant_choice = int(input("➡️  Enter the plant number: ")) - 1
            if 0 <= plant_choice < len(my_garden.plants):
                plant = my_garden.plants[plant_choice]
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
                    my_garden.removePlant(plant)
                    print(f"❌ You removed {plant.name} from the garden.")
            else:
                print("❌ Invalid plant.")
        except ValueError:
            print("❌ Invalid input, please enter a valid number.")

    elif choice == "4":
        print("Select a plant to add:")
        for key, (name, water, light, growth) in available_plants.items():
            print(f"{key}. {name} (Water: {water}, Light: {light}, Growth: {growth})")
        plant_choice = input("➡️  Enter the plant number: ")
        if plant_choice in available_plants:
            name, water, light, growth = available_plants[plant_choice]
            new_plant = Plants(name, water, light, growth)
            my_garden.addPlant(new_plant)
            print(f"🌱 {name} has been added to the garden!")
        else:
            print("❌ Invalid choice.")

    elif choice == "6":
        print("⏭️ Moving to the next day...")
        day += 1
        my_garden.updateLight()
        my_garden.modifPlantsStatus()

    elif choice == "7":
        print("👋 Game over. Thanks for playing!")
        break

    else:
        print("❌ Invalid option, try again.")

    time.sleep(0.5)
