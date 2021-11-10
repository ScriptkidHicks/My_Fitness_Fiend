"""
Filename: app.py

Authors: Jordan Smith
Group: Wholesome as Heck Programmers
Last modified: 11/07/21
"""
import flask
from login import login_page

# Generate the flask app
app = flask.Flask(__name__)
app.register_blueprint(login_page)

@app.route('/test')
def test():
    return "Hello World"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5000", debug=True)

