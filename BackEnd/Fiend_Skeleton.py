"""
Author(s): Niklaas Cotta
Date created: 11/6/21
Team WAHP, CIS422 FA21
Desc:
"""

import time

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


class Level:
    def __init__(self):
        self.value = 1
        self.cap = 3
        self.xp = 0

    def __str__(self):
        return str(self.value)

    def addxp(self, value):

        done = False

        print(f"EXP increased by {value} points!")
        self.xp += value

        while not done:
            prevlevel = self.value

            if self.xp >= self.cap:
                self.levelup()
                print(f"LEVELED UP TO LEVEL {str(self.value)}!!!")

            if self.value == prevlevel:
                done = True

            time.sleep(0.25)

    def levelup(self):
        self.value += 1
        self.xp -= self.cap
        self.resetCap()

    def resetCap(self):
        self.cap = ((4 * self.value ** 3) // 5)


class Fiend:
    def __init__(self, name, type_id, level):
        self.name = name
        self.type_id = type_id
        self.level = level

    def dance(self):
        print(f"{self.name} does a little dance and looks very cute doing it")

    def translateID(self):
        translationTable = {
            0o001: "Leg Monster",
            0o002: "Arm Monster"
        }

        return translationTable[self.type_id]

    def printinfo(self):
        print("==========================================")
        print(f"Name:     {self.name}")
        print(f"Type:     {self.translateID()}")
        print(f"Level:    {str(self.level.value)} (xp: {str(self.level.xp)}/{str(self.level.cap)})")
        print("==========================================\n")


if __name__ == '__main__':
    newLevel = Level()
    myFiend = Fiend("Lil Klokov", 0o001, newLevel)
    myFiend.dance()
    for i in range(5):
        time.sleep(1)
        myFiend.printinfo()
        myFiend.level.addxp(50)

