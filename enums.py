from enum import Enum

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