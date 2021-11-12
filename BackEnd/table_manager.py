"""
Filename: table_manager.py

Purpose: A class to define and create all tables needed in the database

Authors: Jordan Smith
Group: Wholesome as Heck Programmers (WaHP)
Last modified: 11/09/21
"""
from db_manager import db_mgr

DROP_ALL = True

tables = {}

###
#   TABLES TO BE ADDED
###
tables['fitnessGoal'] = {
    'fitness_id': 'int NOT NULL AUTO_INCREMENT',
    'name': 'varchar(16) NOT NULL',
    'constraints': {
        'PRIMARY KEY': 'fitness_id'
    }
}

tables['users'] = {
    'user_id': 'int NOT NULL AUTO_INCREMENT',
    'email': 'varchar(64) NOT NULL',
    'username': 'varchar(64) NOT NULL',
    'password': 'varchar(255) NOT NULL',
    'created_at': 'timestamp DEFAULT CURRENT_TIMESTAMP',
    'last_logged_in': 'timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP',
    'login_streak': 'int NOT NULL DEFAULT 1',
    'monster_id': 'int',
    'height': 'float',
    'weight': 'float',
    'fitness_goal_id': 'int',
    'has_finished_quiz': 'boolean DEFAULT false',
    'wants_emails': 'boolean',
    'show_tooltips': 'boolean DEFAULT true',
    'constraints': {
        'UNIQUE': 'email',
        'UNIQUE': 'username',
        'PRIMARY KEY': 'user_id',
        'FOREIGN KEY': ['fitness_goal_id', 'fitnessGoal(fitness_id)']
    }
}

tables['workouts'] = {
    'workout_id': 'int NOT NULL AUTO_INCREMENT',
    'type': 'varchar(16) NOT NULL',
    'name': 'varchar(32) NOT NULL',
    'workout_difficulty': 'int NOT NULL',
    'is_priority': 'bool NOT NULL',
    'constraints': {
        'PRIMARY KEY': 'workout_id'
    }
}

tables['workoutConnection'] = {
    'workout_connection_id': 'int NOT NULL AUTO_INCREMENT',
    'workout_id': 'int NOT NULL',
    'fitness_goal_id': 'int NOT NULL',
    'constraints': {
        'PRIMARY KEY': 'workout_connection_id',
        'FOREIGN KEY': ['workout_id', 'workouts(workout_id)'],
        'FOREIGN KEY': ['fitness_goal_id', 'fitnessGoal(fitness_id)']
    }
}

tables['workoutTips'] = {
    'tip_id': 'int NOT NULL AUTO_INCREMENT',
    'tip_string': 'varchar(255) NOT NULL',
    'workout_id': 'int',
    'constraints': {
        'PRIMARY KEY': 'tip_id',
        'FOREIGN KEY': ['workout_id', 'workouts(workout_id)']
    }
}

tables['workoutLogs'] = {
    'log_id': 'int NOT NULL AUTO_INCREMENT',
    'user_id': 'int NOT NULL',
    'workout_type_id': 'int NOT NULL',
    'time_created': 'timestamp DEFAULT CURRENT_TIMESTAMP',
    'reps': 'int',
    'sets': 'int',
    'weight': 'float',
    'time_duration': 'float',
    'distance_duration': 'float',
    'details': 'varchar(255) NOT NULL',
    'user_enjoyment': 'int NOT NULL',
    'constraints': {
        'PRIMARY KEY': 'log_id',
        'FOREIGN KEY': ['user_id', 'users(user_id)'],
        'FOREIGN KEY': ['workout_type_id', 'workouts(workout_id)']
    }
}

tables['relationshipType'] = {
    'relationship_type_id': 'int NOT NULL AUTO_INCREMENT',
    'type': 'varchar(32)',
    'constraints': {
        'PRIMARY KEY': 'relationship_type_id'
    }
}

tables['userRelationship'] = {
    'relationship_id': 'int NOT NULL AUTO_INCREMENT',
    'user_first_id': 'int NOT NULL',
    'user_second_id': 'int NOT NULL',
    'type_id': 'int NOT NULL',
    'constraints': {
        'PRIMARY KEY': 'relationship_id',
        'FOREIGN KEY': ['user_first_id', 'users(user_id)'],
        'FOREIGN KEY': ['user_second_id', 'users(user_id)'],
        'FOREIGN KEY': ['type_id', 'relationshipType(relationship_type_id)']
    }
}

tables['userPRs'] = {
    'user_id': 'int NOT NULL',
    'workout_id': 'int NOT NULL',
    'weight': 'float',
    'time': 'float',
    'distance': 'float',
    'constraints': {
        'FOREIGN KEY': ['user_id', 'users(user_id)'],
        'FOREIGN KEY': ['workout_id', 'workouts(workout_id)']
    }
}

tables['monsters'] = {
    'monster_id': 'int NOT NULL AUTO_INCREMENT',
    'name': 'varchar(64) NOT NULL',
    'exp': 'int NOT NULL DEFAULT 0',
    'level': 'int NOT NULL DEFAULT 1',
    'image': 'varchar(32) NOT NULL',
    'constraints': {
        'PRIMARY KEY': 'monster_id'
    }
}

"""
Fitness goals
    Strength increase
    General fitness
    Weight Loss
"""


# Drop all of the tables for debugging and configuration
if DROP_ALL:
    db_mgr.drop_tables(list(tables.keys())[::-1])

# Add the tables into the database
for table_name, table_description in tables.items():
    db_mgr.create_table(table_name, table_description)
