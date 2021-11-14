"""
Filename: app.py

Authors: Jordan Smith
Group: Wholesome as Heck Programmers
Last modified: 11/13/21
"""
import flask
from login import login_page
from db_manager import db_mgr

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
    from monsters LEFT JOIN users ON monsters.monster_id = users.monster_id 
    WHERE users.user_id = {user_id};
    """
    user_monster_info = db_mgr.submit_query(sql_query)[0]

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
app.route("/get_user_info")
def user_info():
    request_data = json.loads(flask.request.data)

    return get_user_monster_info(request_data['user_id'])

@app.route("/level_monster_up")
def monster_level_up():
    request_data = json.loads(flask.request.data)

    # Probably do something with the fiend class

    return get_user_monster_info(request_data['user_id'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5000", debug=True)

