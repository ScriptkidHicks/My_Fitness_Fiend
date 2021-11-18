"""
Filename: app.py

Authors: Jordan Smith
Group: Wholesome as Heck Programmers
Last modified: 11/16/21
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

        value_results = db_mgr.get_all_rows(table, arg_columns, where_options=where_options_local)
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

def post_results(table, data, id_name, id_value):
    # Make sure the data is a dictionary
    if (type(data) is not dict):
        abort(404, message="Error: Data must be a dictionary")

    update_results = db_mgr.update_rows(table, data, where_options={id_name: id_value})

    if (update_results):
        return {"message": f"Row {id_value} of {table} has been updated"}, 201
    return {"message": f"Row {id_value} of {table} could not be updated"}, 500

    

###
#   Rest API Endpoint classes
#       get     -> Used to get back data (takes in an id from the uri and wants list data for columns)
#       post    -> Used to update data   (takes in an id from the uri and wants dict data for new data)
#       put     -> Used to create data   (wants data to store)
###
class UserInfo(Resource):
    def get(self, user_id):
        # Try to get arguments from the data
        try:
            args = json.loads(flask.request.data)
        except json.decoder.JSONDecodeError:    # If data is not sent in the request, set the columns to be all
            args = {}
            args['columns'] = [col[0] for col in db_mgr.get_table_columns("users")]
            
        return get_results("users", args['columns'], "user_id", user_id), 201

    def post(self, user_id):
        # Get the data from the request
        data = json.loads(flask.request.data)
        return post_results("users", data, "user_id", user_id)

class ApiInfoPoint(Resource):
    def get(self, table_name):
        args = json.loads(flask.request.data)
        
        # If no where specifiers are sent, just leave it as an empty dict
        if not args.has_key("where"):
            args['where'] = {}

        # If column data was not sent, use all of the columns from the table
        if not args.has_key("columns"):
            args['columns'] = [col[0] for col in db_mgr.get_table_columns(table_name)]

        return get_results(table_name, args['columns'], args['where']), 201

        

# class MonsterInfo(Resource):
#     def get(self, monster_id):
#         # Try to get arguments from the data
#         try:
#             args = json.loads(flask.request.data)
#         except json.decoder.JSONDecodeError:    # If data is not sent in the request, set the columns to be all
#             args = {}
#             args['columns'] = [col[0] for col in db_mgr.get_table_columns("users")]
        
#         return get_results("monsters", args['columns'], "monster_id", monster_id)

#api.add_resource(UserInfo, '/api/users/<int:user_id>')

api.add_resource(ApiInfoPoint, '/api/<table_name>')

# @app.route('/test')
# def test():
#     return "Hello World"

# """
# Endpoint to reset a user's quiz status (FOR TESTING)
#     Returns 201 on success, 500 on failure
# """
# @app.route("/reset_user_quiz")
# def reset_quiz():
#     user_id = flask.request.headers.get("user_token")

#     res = db_mgr.update_rows("users", {"has_finished_quiz": False}, where_options={"user_id": user_id})

#     if res:
#         return {'message': 'success'}, 201
#     else:
#         return {'message': 'failure'}, 500

# @app.route("/submit_user_quiz")
# def submit_user_quiz():
#     request_data = json.loads(flask.requests.data)

#     user_id = int(request_data["user_id"])
#     quiz_results = request_data["quiz_results"]

#     return {}, 201

# """
# Endpoint to get all of the fitness goals listed in the database
# """
# @app.route("/get_all_fitness_goals")
# def get_fitness_goals():
#     fitness_goals = db_mgr.get_all_rows("fitnessGoal", "name")

#     return fitness_goals

# """
# Endpoint to update the user's information
#     Returns 201 on success, 500 on failure
# """
# @app.route("/update_user_info", methods=["POST"])
# def update_user_info():
#     request_data = json.loads(flask.request.data)

#     user_id = int(request_data['user_id'])
#     updated_info = request_data['updated_info']

#     updated_result = db_mgr.update_rows("users", 
#                                         updated_info,
#                                         where_options={'user_id': user_id}
#                                         )

#     if not updated_result:
#         return {"message": "User data could not be updated"}, 500
    
#     return {"message": "User data has been updated"}, 201

# """
# Endpoint to get specific columns from the user database
#     Mainly for testing
# """
# @app.route("/get_specific_user_info", methods=["GET"])
# def get_specific_user_info():
#     request_data = json.loads(flask.request.data)

#     user_id = int(request_data['user_id'])
#     data = request_data['data']

#     retrieval_result = db_mgr.get_one_row("users", data, where_options={'user_id': user_id})

#     if not retrieval_result:
#         return {"message": "Data could not be retrieved"}, 500

#     return {"data": retrieval_result}, 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5000", debug=True)

