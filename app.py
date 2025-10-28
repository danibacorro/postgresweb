from flask import Flask
from funciones import *

app = Flask(__name__)
app.secret_key = 'root'

@app.route('/', methods=['GET', 'POST'])
def login():
    return login_func()

@app.route('/tables')
def tables():
    return tables_func()

@app.route('/table/<name>')
def table_data(name):
    return table_data_func(name)

if __name__ == '__main__':
    app.run(debug=True)

