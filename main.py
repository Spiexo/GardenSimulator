import time

class Garden:
    def __init__(self):
        self.plants = []

    def addPlant(self, plant):
        self.plants.append(plant)

    def checkPlantsStatus(self):
        for plant in self.plants:
            plant.updateStatus()
            plant.notifyPlayer()

class Plants:
    def __init__(self, name, waterRequir, light, growth):
        self.waterNeed = waterRequir
        self.lightNeed = light
        self.growthSpeed = growth
        self.name = name
        self.water = 50
        self.light = 50
        self.health = 100
        self.maturity = 0

    def waterPlant(self, amount):
        self.water += amount
        self.water = max(0, min(self.water, 100))

    def fertilize(self):
        self.maturity += self.growthSpeed * 2
        self.maturity = min(self.maturity, 100)

    def lightSpot(self, amount):
        self.light += amount
        self.light = max(0, min(self.light, 100))

    def maintain(self):
        self.health += 40
        self.health = min(self.health, 100)

    def updateStatus(self):
        if self.water < self.waterNeed - 20:
            self.health -= 10
        elif self.water > self.waterNeed + 20:
            self.health -= 5

        if self.light < self.lightNeed - 20:
            self.health -= 10
        elif self.light > self.lightNeed + 20:
            self.health -= 5

        if self.health > 50 and abs(self.water - self.waterNeed) < 20 and abs(self.light - self.lightNeed) < 20:
            self.maturity += self.growthSpeed
            self.maturity = min(self.maturity, 100)

        if self.health <= 0:
            self.health = 0
            print(f"❌ {self.name} has died!")

    def notifyPlayer(self):
        print(f"\n🌱 {self.name} - Health: {self.health}%, Water: {self.water}%, Light: {self.light}%, Maturity: {self.maturity}%")
        print(f" {self.name} needs Water: {self.waterNeed}%, Light: {self.lightNeed}%. Possede Growth: {self.growthSpeed}%")
        if self.health < 50:
            print(f"⚠️ {self.name} is in poor health!")
        if self.water < self.waterNeed - 20:
            print(f"💧 {self.name} needs water!")
        if self.light < self.lightNeed - 20:
            print(f"🔆 {self.name} needs light!")
        if self.maturity >= 100:
            print(f"🎉 {self.name} is fully matured!")

# List of available plants
available_plants = {
    "1": ("Tomato", 60, 70, 5),
    "2": ("Carrot", 50, 60, 4),
    "3": ("Lettuce", 40, 50, 3)
}

my_garden = Garden()
day = 1

while True:
    print(f"\n🌞 Day {day}")
    my_garden.checkPlantsStatus()

    print("\nWhat would you like to do?")
    print("1️⃣  Water a plant")
    print("2️⃣  Fertilize a plant")
    print("3️⃣  Give light to a plant")
    print("4️⃣  Maintain a plant")
    print("5️⃣  Add a plant")
    print("6️⃣  Skip to the next day")
    print("7️⃣  Quit")

    choice = input("➡️  Your choice: ")

    if choice in ["1", "2", "3", "4"] and my_garden.plants:
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
                    amount = int(input("🔆 How much light to give?: "))
                    plant.lightSpot(amount)
                elif choice == "4":
                    plant.maintain()
                    print(f"✂️ You maintained {plant.name}!")
            else:
                print("❌ Invalid plant.")
        except ValueError:
            print("❌ Invalid input, please enter a valid number.")

    elif choice == "5":
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

    elif choice == "7":
        print("👋 Game over. Thanks for playing!")
        break

    else:
        print("❌ Invalid option, try again.")

    time.sleep(0.5)