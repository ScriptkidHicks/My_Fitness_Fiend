'''
code: Creating the Workout classes and subclasses
group: Workout assistance Program
author(s): Thomas Joyce
last modified: 04 Nov 2021
'''

from collections import defaultdict

class Workout:
    def __init__(self):
        self.exercises = defaultdict(list)


class Strength:
    '''
    parent class for strength workouts
    reps, sets, and days per week set to default
    '''
    def __init__(self, reps=8, sets=3, name=None, days=3):
        self.reps = reps
        self.sets = sets
        self.name = name
        self.days = days
    
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
    def __init__(self, weight=0.8, intensity="medium"):
        self.weight = weight
        self.intesity = intensity

    def __repr__(self):
        return "test"
    
    def __str__(self):
        return "test"

    def generate_Workout(self):
        if self.intesity == "light":
            #TODO
            return None
        elif self.intesity == "medium":
            #todo
            return None
        else:
            #todo
            return None

    def fetch_Workout(self, category):
        '''
        pass category as string of workout type (ie, chest)
        will call for a workout from the database of that type
        '''
        #TODO
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