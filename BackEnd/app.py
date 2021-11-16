"""
Filename: app.py

Authors: Jordan Smith
Group: Wholesome as Heck Programmers
Last modified: 11/13/21
"""
import flask
from login import login_page
from db_manager import db_mgr
import json

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
    user_monster_info = db_mgr.submit_query(sql_query)[0]

    # The user doesn't have a monster
    if (user_monster_info == []):
        user_monster_info = [None for _ in range(len(desired_columns) - 1)]
        #user_monster_info += db_mgr.get_one_row('users', 'has_finished_quiz', {'user_id': user_id})

    # Transform results into a dictionary and return
    monster_data = {}
    for i in range(len(desired_columns)):
        monster_data[desired_columns[i]] = user_monster_info[i]

    return monster_data



@app.route('/test')
def test():
    return "Hello World"

"""
account info
    monster info (species, level, exp)
    has done survey
"""
@app.route("/get_user_info", methods=["GET"])
def user_info():
    user_id = flask.request.headers.get("user_token")

    return get_user_monster_info(user_id), 201

@app.route("/level_monster_up", methods=["GET"])
def monster_level_up():
    user_id = flask.request.headers.get("user_token")

    # Probably do something with the fiend class

    return get_user_monster_info(user_id), 201

@app.route("/reset_user_quiz")
def reset_quiz():
    user_id = flask.request.headers.get("user_token")

    res = db_mgr.update_rows("users", {"has_finished_quiz": False}, where_options={"user_id": user_id})

    if res:
        return {'message': 'success'}, 201
    else:
        return {'message': 'failure'}, 500

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5000", debug=True)

