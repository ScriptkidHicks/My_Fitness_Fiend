'''
code: Creating the Workout classes and subclasses
group: Workout assistance Program
author(s): Thomas Joyce
last modified: 11 Nov 2021
'''
import random
import time
from db_manager import *
from collections import defaultdict


class Workout:
    def __init__(self, name=None):
        self.name = name
        self.exercises = defaultdict(list)

    def fetch_Workout(self, category):
        '''
        pass category as string of workout type (ie, chest)
        will call for a workout from the database of that type
        '''
        exercise = db_mgr.get_all_rows("Workouts","name",\
                                      {"type": category,"priority":1},["and"])
        return exercise
    
    def populate_plan(self):
        for key in self.exercises:
            self.exercises[key] = self.fetch_Workout(key)


class fullBody(Workout):
    def __init__(self):
        self.name = "Full Body"
        self.exercises = {"Chest":[], "Shoulders":[], "Bicep":[], "Tricep":[],\
                          "Upper Back":[], "Lower Back":[], "Butt":[],\
                          "Thighs":[], "Hamstrings":[], "Calves":[]}
        self.populate_plan()


class Strength:
    '''
    parent class for strength workouts
    reps, sets, and days per week set to default
    '''
    def __init__(self, reps=8, sets=3, name=None, days=3, goal="general",\
                 intensity="medium"):
        self.reps = reps
        self.sets = sets
        self.name = name
        self.days = days
        self.goal = goal
        self.intesity = intensity
        if self.intesity == "light":
            self.weight = 0.6
        elif self.intesity == "medium":
            self.weight = 0.7
        else:
            self.weight = 0.8
        
    def __repr__(self):
        return "test"
    
    def __str__(self):
        return "test"


class Cardio:
    '''
    pass duration in minutes as an int 
    pass intesity in as a str, light, medium, heavy for type of workout
    '''
    def __init__(self, name=None, duration=30, intensity="medium"):
        self.name = name
        self.duration = duration
        self.intensity = intensity
    
    def __repr__(self):
        return "test"
    
    def __str__(self):
        return "test"


class Weights(Strength):
    '''
    pass weight in as a float range(0,1) for weight calculations
    pass intesity in as a str, light, medium, heavy for type of workout

    '''
    def __init__(self, plan=fullBody()):
        self.plan = plan

    def __repr__(self):
        return "test"
    
    def __str__(self):
        return "test"

    def generate_Workout(self):
        if self.goal == "general":
            self.plan = fullBody()
        elif self.goal == "Strength":
            #todo
            return None
        else:
            #todo
            return None


class Calisthenics(Strength):
    def __init__(self, duration=None):
        self.duration = duration

    def __repr__(self):
        return "test"
    
    def __str__(self):
        return "test"

    
if __name__ == "__main__":
    w = Weights()
    print(w)