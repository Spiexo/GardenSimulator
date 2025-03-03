from garden import Garden
from game import mainLoop

if __name__ == "__main__":
    myGarden = Garden()
    myGarden.difficulty()
    mainLoop(myGarden)