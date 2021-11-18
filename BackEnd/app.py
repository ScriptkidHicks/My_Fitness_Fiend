"""
Filename: app.py

Authors: Jordan Smith
Group: Wholesome as Heck Programmers
Last modified: 11/18/21
"""
import flask
from flask_restful import reqparse, abort, Api, Resource
from login import login_page
from monster_endpoints import monster_page
from db_manager import db_mgr
import json
import datetime

# Generate the flask app
app = flask.Flask(__name__)
app.register_blueprint(login_page)
app.register_blueprint(monster_page)

# Generate the Api instance
api = Api(app)

# List of table names for abort errors
db_tables = db_mgr.get_tables()

###
#   Helper API functions
###
def get_results(table, arg_columns, where_specifiers, id_name=None, id_value=None):
    try:
        # The id_name and the id_value are optional
        where_options_local = where_specifiers
        if (id_name is not None and id_value is not None):
            where_options_local[id_name] = id_value

        # Specify the AND connections
        and_connections = ["AND" for _ in range(len(where_options_local) - 1)]

        value_results = db_mgr.get_all_rows(table, arg_columns, where_options=where_options_local, where_connectors=and_connections)
    except TypeError:
        abort(500, message="Error: Failure parsing arguments")

    # Store the results in a json format
    json_result = {}
    for row_count, row in enumerate(value_results):
        curr_row = {}
        for col_count, column in enumerate(arg_columns):
            val = row[col_count]

            # If the value returned is a date, we need to convert it to a string 
            if (isinstance(val, datetime.datetime)):
                curr_row[column] = val.strftime("%d/%m/%Y, %H:%M:%S")
            else:
                curr_row[column] = val

        # Append the current json dictionary to the overall dict
        json_result[row_count] = curr_row
    
    return json_result

def post_results(table, data, where_specifiers, id_name=None, id_value=None):
    # Make sure the data is a dictionary
    if (type(data) is not dict):
        abort(404, message="Error: Data must be a dictionary")

    where_options_local = where_specifiers
    if (id_name is not None and id_value is not None):
        where_options_local[id_name] = id_value

    # Specify the AND connections
    and_connections = ["AND" for _ in range(len(where_options_local) - 1)]

    update_results = db_mgr.update_rows(table, data, where_options=where_options_local, where_connectors=and_connections)

    if (update_results):
        return {"message": f"Rows of {table} has been updated"}, 201
    return {"message": f"Rows of {table} could not be updated"}, 500

    

###
#   Rest API Endpoint classes
#       get     -> Used to get back data (takes in an id from the uri and wants list data for columns)
#       post    -> Used to update data   (takes in an id from the uri and wants dict data for new data)
#       put     -> Used to create data   (wants data to store)
###
class ApiInfoPointSpec(Resource):
    def get(self, table_name, id):
        # Try to get the arguments to the user
        try: 
            args = json.loads(flask.request.data)
        except json.decoder.JSONDecodeError:
            args = {}

        # If no where specifiers are sent, just leave it as an empty dict
        if "where" not in args:
            args['where'] = {}

        # If column data was not sent, use all of the columns from the table
        if "columns" not in args:
            args['columns'] = [col[0] for col in db_mgr.get_table_columns(table_name)]

        primary_key = db_mgr.get_table_primary_key(table_name)

        return get_results(table_name, args['columns'], args['where'], primary_key, id), 201

    def post(self, table_name, id):
        args = json.loads(flask.request.data)

        # Throw a fit if data is not sent
        if "data" not in args:
            abort(404, "Data is required for POST method")

        # If no where specifiers are sent, just leave it as an empty dict
        if "where" not in args:
            args['where'] = {}

        primary_key = db_mgr.get_table_primary_key(table_name)

        return post_results(table_name, args['data'], args['where'], primary_key, id), 201


class ApiInfoPoint(Resource):
    def get(self, table_name):
        # Try to get the arguments to the user
        try: 
            args = json.loads(flask.request.data)
        except json.decoder.JSONDecodeError:
            args = {}
        
        # If no where specifiers are sent, just leave it as an empty dict
        if "where" not in args:
            args['where'] = {}

        # If column data was not sent, use all of the columns from the table
        if "columns" not in args:
            args['columns'] = [col[0] for col in db_mgr.get_table_columns(table_name)]

        return get_results(table_name, args['columns'], args['where']), 201

    def post(self, table_name):
        args = json.loads(flask.request.data)

        # Throw a fit if data is not sent
        if "data" not in args:
            abort(404, "Data is required for POST method")

        # If no where specifiers are sent, just leave it as an empty dict
        if "where" not in args:
            args['where'] = {}

        return post_results(table_name, args['data'], args['where']), 201

api.add_resource(ApiInfoPoint, '/api/<table_name>')
api.add_resource(ApiInfoPointSpec, '/api/<table_name>/<int:id>')

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

