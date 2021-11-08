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
        self.cap = 4
        self.xp = 0

    def __str__(self):
        return str(self.value)

    def addxp(self, value):
        self.xp += value
        if self.xp >= self.cap:
            self.levelup()
            print(f"LEVELED UP TO LEVEL {str(self.value)}!!!")
        else:
            print("Not enough XP :(")

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


if __name__ == '__main__':
    newLevel = Level()
    myFiend = Fiend("Lil Klokov", 0o001, newLevel)
    myFiend.dance()
    for i in range(5):
        time.sleep(2)
        print("Current Level: " + str(myFiend.level.value))
        print("XP: " + str(myFiend.level.xp) + "/" + str(myFiend.level.cap))
        print("adding 10 experience points...")
        myFiend.level.addxp(10)

