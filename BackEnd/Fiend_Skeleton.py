"""
Author(s): Niklaas Cotta
Date created: 11/6/21
Team WAHP, CIS422 FA21
Desc:
"""

from time import *
import sys

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
1) Decorator??
2) EXP rewarded w/ workout log entry is functional
"""

bestiary = {"01": "Baby",
            "02": "Juvenile",
            "03": "Normal",
            "04": "Mature",
            "05": "Magnificent",
            "06": "Geriatric",
            "07": "Ascended"}


def delay_print(s, delay):
    # print one character at a time
    # https://stackoverflow.com/questions/9246076/how-to-print-one-character-at-a-time-on-one-line
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        sleep(delay)


def testFiend():
    myFiend = Fiend()
    myFiend.printinfo()
    for i in range(5):
        sleep(0.5)
        print(f"\nStep: {i+1}")
        myFiend.updateXP(50)
    myFiend.printinfo()
    # myFiend.seppuku()


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

    def resetCap(self):
        self.xpCap = ((4 * self.value ** 3) // 5)


class Fiend:
    def __init__(self, nickname="Thammash Smotta", species="Kettlehell", species_id="KM01", level=Level()):  # :)
        self.nickname = nickname
        self.species = species
        self.id = species_id
        self.level = level

    def dance(self):
        print(f"{self.nickname} does a little dance and looks very cute doing it")

    def tellLevel(self):
        return self.level.value

    def updateXP(self, value):
        leveled = self.level.incrementXP(value)
        evolveLevel = 5
        toEvolve = self.level.value % evolveLevel
        if toEvolve == 0 and leveled > 0:
            self.transform()

    def transform(self):
        print(f"{self.nickname} is evolving!!!")
        for _ in range(3):
            sleep(0.5)
            print("  .  ")

        newFormInt = int(self.id[3]) + 1
        self.id = self.id[0:3] + str(newFormInt) + self.id[4:]  # dont ask me
        print(f"{self.species} grew into it's {bestiary[self.id[2:]]} form!!!")

        return self.species

    def seppuku(self):
        delay_print("私は名誉をもって人生を送ってきました。 私は何も後悔していない...\n", 0.15)
        sleep(1)
        delay_print("死  DEATH  死\n", 0.25)
        sleep(1)
        del self

    def printinfo(self):
        print("==========================================")
        print(f"Name:     {self.nickname}")
        print(f"Species:  {self.species} ({bestiary[self.id[2:]]})")
        print(f"Level:    {str(self.level.value)} (xp: {str(self.level.xp)}/{str(self.level.xpCap)})")
        print("==========================================\n")


if __name__ == '__main__':
    testFiend()
