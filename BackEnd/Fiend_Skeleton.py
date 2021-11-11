"""
Author(s): Niklaas Cotta
Date created: 11/6/21
Team WAHP, CIS422 FA21
Desc:
"""

from time import *

"""
Hierarchy
- Strength Class (base):
    name (str):  name of the workout
    reps (int):  number of reps for workout
    sets (int):  number of sets for workout
    days (int):  ?

    - Weights Class:
        weight (int):     how heavy you're lifting
        intensity (str):  scale weight based on intensity level
    - Calisthenics Class:
        duration (int):   how long you perform the workout

- Cardio Class:
    name (str):       name of cardio workout
    duration (int):   how long you perform the workout
    intensity (int):  how intense the workout was
"""

"""
TODO:
1) Image attribute implementation
2) Global dictionary bestiary
3) Evolution() method
    - Need to figure out species stuff first
4) Decorator??
"""


class Level:
    def __init__(self):
        self.value = 1
        self.xpCap = 3
        self.xp = 0

    def __str__(self):
        return str(self.value)

    def incrementXP(self, value):
        done = False
        oldLevel = self.value

        print(f"EXP increased by {value} points!")
        self.xp += value

        while not done:
            prevLevel = self.value

            if self.xp >= self.xpCap:  # levelup
                self.levelUp()
                print(f"LEVELED UP TO LEVEL {str(self.value)}!!!")

            if self.value == prevLevel:
                done = True

            sleep(0.25)

        return self.value - oldLevel  # how much you leveled up

    def levelUp(self):
        self.value += 1
        self.xp -= self.xpCap
        self.resetCap()

    # def levelDown(self):

    def resetCap(self):
        self.xpCap = ((4 * self.value ** 3) // 5)


class Fiend:
    def __init__(self, name, species, level):
        self.name = name
        self.species = species
        self.level = level

    def dance(self):
        print(f"{self.name} does a little dance and looks very cute doing it")

    def updateXP(self, value):
        leveled = self.level.incrementXP(value)
        if leveled > 0:
            # check if ready to transform
            # if so, evolve
            pass

    def transform(self):
        prevName = self.name
        print(f"{self.name} is evolving!!!")
        for _ in range(3):
            sleep(0.25)
            print("  .  ")
        # find next species (KM1 -> KM2 -> ...)
        # set new species
        # fetch image of species and set new image
        print(f"{prevName} evolved into ... {self.name}!!!")

    def printinfo(self):
        print("==========================================")
        print(f"Name:     {self.name}")
        print(f"Species:  {self.species}")
        print(f"Level:    {str(self.level.value)} (xp: {str(self.level.xp)}/{str(self.level.xpCap)})")
        print("==========================================\n")


if __name__ == '__main__':
    newLevel = Level()
    myFiend = Fiend("Kloks", "KM01", newLevel)
    for i in range(5):
        sleep(0.5)
        myFiend.printinfo()
        myFiend.updateXP(50)
