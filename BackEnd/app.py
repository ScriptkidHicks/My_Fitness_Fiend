"""
Filename: app.py

Authors: Jordan Smith
Group: Wholesome as Heck Programmers
Last modified: 11/16/21
"""
import flask
from login import login_page
from monster_endpoints import monster_page
from db_manager import db_mgr
import json
from Fiend_Skeleton import *

# Generate the flask app
app = flask.Flask(__name__)
app.register_blueprint(login_page)
app.register_blueprint(monster_page)


@app.route('/test')
def test():
    return "Hello World"

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

@app.route("/submit_user_quiz")
def submit_user_quiz():
    request_data = json.loads(flask.requests.data)

    user_id = int(request_data["user_id"])
    quiz_results = request_data["quiz_results"]

    return {}, 201

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

