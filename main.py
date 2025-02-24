class Garden:
    def __init__(self):
        self.plants = []

    def addPlant(self, plant):
        self.plants.append(plant)

    def checkPlantsStatus(self):
        for plant in self.plants:
            plant.updateStatus()
            plant.notifyPlayer()

class Plants(Garden):
    def __init__(self, name, waterRequir, light, growth):
        self.waterNeed = waterRequir # plant stat //
        self.lightNeed = light
        self.growthSpeed = growth
        self.name = name
        self.water = 50 # palnt base stat //
        self.light = 50
        self.health = 100
        self.maturity = 0

    def waters(self, amount):
        self.water += amount
        if self.water > 100:
            self.water = 100
        elif self.water < 0:
            self.water = 0

    def fertilizes(self):
        self.maturity += self.growthSpeed * 2
        if self.maturity > 100:
            self.maturity = 100

    def maintain(self):
        self.health += 40
        if self.health > 100:
            self.health = 100

    def updateStatus(self) :
        if self.water < self.waterNeed - 20:
            self.health -= 50
        elif self.water > self.waterNeed + 20:
            self.health -= 30

        if self.light < self.lightNeed - 20:
            self.health -= 50
        elif self.light > self.lightNeed + 20:
            self.health -= 30

        if abs(self.water - self.water) < 10 and abs(self.light - self.lightNeed) < 10:
            self.maturity += self.growthSpeed

        if self.health <= 0:
            self.health = 0
            print(f"Warning !!!\n{self.name} is dead !")


    def notifyPlayer(self):
        if self.health < 50:
            print(f"⚠️ Warning !!! {self.name} est en mauvaise santé ({self.health}%).")
        if self.water < self.waterNeed - 10:
            print(f"💧 Warning !!! {self.name} a besoin d'eau !")
        if self.water > self.waterNeed + 10:
            print(f"⚠️ Warning !!! {self.name} a trop d'eau, attention à la pourriture !")
        if self.maturity >= 100:
            print(f"🌿 Warning !!! {self.name} est mature !")

# Test
my_garden = Garden()
tomato = Plants("Tomate", waterRequir=60, light=70, growth=5)
my_garden.addPlant(tomato)


for _ in range(1):
    tomato.waters(-10)
    my_garden.checkPlantsStatus()
    print("---")