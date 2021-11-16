"""
Filename: app.py

Authors: Jordan Smith
Group: Wholesome as Heck Programmers
Last modified: 11/16/21
"""
import flask
from login import login_page
from db_manager import db_mgr
import json
from Fiend_Skeleton import *

# Generate the flask app
app = flask.Flask(__name__)
app.register_blueprint(login_page)

# Helper functions
def get_user_monster_info(user_id):
    # Columns we want to pull from
    desired_columns = ['name', 'species', 'exp', 'level', 'has_finished_quiz']

    # Query that is a bit more complicated than the 
    #   db_mgr can handle
    sql_query = f"""
    SELECT {", ".join(desired_columns)}
    from monsters left join users on monsters.user_id = users.user_id
    WHERE users.user_id = {int(user_id)};
    """
    user_monster_info = db_mgr.submit_query(sql_query)

    # The user doesn't have a monster
    if (user_monster_info == []):
        user_monster_info = [None for _ in range(len(desired_columns) - 1)]
        user_monster_info += db_mgr.get_one_row('users', 'has_finished_quiz', {'user_id': int(user_id)})

    # Transform results into a dictionary and return
    monster_data = {}
    for i in range(len(desired_columns)):
        monster_data[desired_columns[i]] = user_monster_info[i]

    return monster_data



@app.route('/test')
def test():
    return "Hello World"

"""
Endpoint to get the user's monster info from the database as well as whether or not
    the user has finished the initial quiz
"""
@app.route("/get_user_info", methods=["GET"])
def user_info():
    user_id = flask.request.headers.get("user_token")

    return get_user_monster_info(user_id), 201

"""
Endpoint to level the user's monster up and return the monster's info and quiz status
    Returns 201 if succeeds,
            409 if the user doesn't have a monster,
            500 if the update fails 
"""
@app.route("/level_monster_up", methods=["GET"])
def monster_level_up():
    user_id = flask.request.headers.get("user_token")

    monster_info = get_user_monster_info(user_id)
    
    if monster_info["name"] is None:
        return {'message': 'User does not have a monster'}, 409

    # Probably do something with the fiend class
    currFiend = Fiend(nickname=monster_info["name"],
                      species=monster_info['species'],
                      level=monster_info['level'])
    currFiend.level.levelUp()

    # Update the info in the monster database
    update_res = db_mgr.update_rows("monsters",
                                   {"level": currFiend.tellLevel()},
                                   where_options={"user_id": int(user_id)}
                                   )
    if not update_res:
        return {"message": "Monster could not be leveled up"}, 500

    monster_info["level"] = int(monster_info["level"]) + 1

    return monster_info, 201

"""
Endpoint to reset a user's quiz status (FOR TESTING)
    Returns 201 on success, 500 on failure
"""
@app.route("/reset_user_quiz")
def reset_quiz():
    user_id = flask.request.headers.get("user_token")

    res = db_mgr.update_rows("users", {"has_finished_quiz": False}, where_options={"user_id": user_id})

    if res:
        return {'message': 'success'}, 201
    else:
        return {'message': 'failure'}, 500

"""
Initializes a monster for a user in the database
    Returns 201 if succeeds,
            409 if the user already has a monster
"""
@app.route("/create_monster_for_user", methods=["POST"])
def create_monster():
    request_data = json.loads(flask.request.data)

    user_id = int(request_data['user_id'])
    monster_data = request_data['monster_info']

    # Check if the user already has a monster 
    user_monsters = db_mgr.get_all_rows('monsters',
                                        'monster_id',
                                        {'user_id': user_id}
                                        )
    if (len(user_monsters) > 0):
        return {"message": "User already has a monster"}, 409

    # Insert the new monster into the database
    monster_data['user_id'] = user_id
    insert_result = db_mgr.add_one_row('monsters', monster_data)

    print(insert_result)

    return {"message": "success"}, 201

"""
Endpoint to get all of the fitness goals listed in the database
"""
@app.route("/get_all_fitness_goals")
def get_fitness_goals():
    fitness_goals = db_mgr.get_all_rows("fitnessGoal", "name")

    return fitness_goals

"""
Endpoint to update the user's information
    Returns 201 on success, 500 on failure
"""
@app.route("/update_user_info", methods=["POST"])
def update_user_info():
    request_data = json.loads(flask.request.data)

    user_id = int(request_data['user_id'])
    updated_info = request_data['updated_info']

    updated_result = db_mgr.update_rows("users", 
                                        updated_info,
                                        where_options={'user_id': user_id}
                                        )

    if not updated_result:
        return {"message": "User data could not be updated"}, 500
    
    return {"message": "User data has been updated"}, 201

"""
Endpoint to get specific columns from the user database
    Mainly for testing
"""
@app.route("/get_specific_user_info", methods=["GET"])
def get_specific_user_info():
    request_data = json.loads(flask.request.data)

    user_id = int(request_data['user_id'])
    data = request_data['data']

    retrieval_result = db_mgr.get_one_row("users", data, where_options={'user_id': user_id})

    if not retrieval_result:
        return {"message": "Data could not be retrieved"}, 500

    return {"data": retrieval_result}, 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5000", debug=True)

