from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "hola mundo"


@app.route('/fail2ban/show', methods='GET')
def show():
    pass


@app.route('/fail2ban/ban/<ip>', methods='GET')
def ban():
    pass


@app.route('/fail2ban/unban/<ip>', methods='GET')
def unban():
    pass


if __name__ == '__main__':
    app.run(debug=True)
