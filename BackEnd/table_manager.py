"""
Filename: table_manager.py

Purpose: A class to define and create all tables needed in the database

Authors: Jordan Smith
Group: Wholesome as Heck Programmers
Last modified: 11/07/21
"""
from db_manager import db_mgr

DROP_ALL = True

tables = {}

###
#   TABLES TO BE ADDED
###
tables['fitnessGoal'] = {
    'fitness_id': 'int NOT NULL AUTO_INCREMENT',
    'name': 'varchar(32) NOT NULL',
    'constraints': {
        'PRIMARY KEY': 'fitness_id'
    }
}

tables['users'] = {
    'user_id': 'int NOT NULL AUTO_INCREMENT',
    'email': 'varchar(64) NOT NULL',
    'password': 'varchar(255) NOT NULL',
    'created_at': 'timestamp DEFAULT CURRENT_TIMESTAMP',
    'last_logged_in': 'timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP',
    'login_streak': 'int NOT NULL DEFAULT 1',
    'monster_id': 'int',
    'height': 'float',
    'weight': 'float',
    'fitness_goal_id': 'int',
    'has_finished_quiz': 'boolean',
    'wants_emails': 'boolean',
    'constraints': {
        'UNIQUE': 'email',
        'PRIMARY KEY': 'user_id',
        'FOREIGN KEY': ['fitness_goal_id', 'fitnessGoal(fitness_id)']
    }
}

tables['workoutTypes'] = {
    'workout_id': 'int NOT NULL AUTO_INCREMENT',
    'fitness_goal_id': 'int NOT NULL',
    'workout_difficulty': 'int NOT NULL',
    'constraints': {
        'PRIMARY KEY': 'workout_id',
        'FOREIGN KEY': ['fitness_goal_id', 'fitnessGoal(fitness_id)'],
    }
}

tables['wodkoutTips'] = {
    'tip_id': 'int NOT NULL AUTO_INCREMENT',
    'tip_string': 'varchar(255) NOT NULL',
    'workout_id': 'int',
    'constraints': {
        'PRIMARY KEY': 'tip_id',
        'FOREIGN KEY': ['workout_id', 'workoutTypes(workout_id)']
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
        'FOREIGN KEY': ['workout_type_id', 'workoutTypes(workout_id)'],
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
        'FOREIGN KEY': ['workout_id', 'workoutTypes(workout_id)']
    }
}

tables['monsters'] = {
    'monster_id': 'int NOT NULL AUTO_INCREMENT',
    'name': 'varchar(64)',
    'exp': 'int',
    'level': 'int',
    'constraints': {
        'PRIMARY KEY': 'monster_id'
    }
}


# Drop all of the tables for debugging and configuration
if DROP_ALL:
    db_mgr.drop_tables(list(tables.keys())[::-1])

# Add the tables into the database
for table_name, table_description in tables.items():
    db_mgr.create_table(table_name, table_description)
