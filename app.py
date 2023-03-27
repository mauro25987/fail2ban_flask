from flask import Flask, jsonify, render_template
import subprocess

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    command = ['docker', 'exec', '-it', 'jovial_bhaskara', 'sqlite3',
               '/var/lib/fail2ban/fail2ban.sqlite3',
               'select ip,jail from bips']
    process = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding='UTF-8'
        )
    return render_template('index.html', data=process.stdout)


@app.route('/fail2ban/ban/<ip>', methods=['GET'])
def add_ban(ip):
    command = ['fail2ban-client', 'set', 'sshd', ip]
    process = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="UTF-8"
        )
    return jsonify(result=process.stdout)


@app.route('/fail2ban/unban/<ip>', methods=['GET'])
def remove_ban(ip):
    command = ['fail2ban-client', 'unban', ip]
    process = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="UTF-8"
        )
    return jsonify(result=process.stdout)


if __name__ == '__main__':
    app.run(debug=True)
