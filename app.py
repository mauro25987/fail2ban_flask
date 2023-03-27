from flask import (
    Flask, jsonify, render_template, request, redirect, url_for, flash
)
from requests import get
from dotenv import load_dotenv
import subprocess
import os

load_dotenv()
host = os.environ['HOST']
route1 = os.environ['ROUTE1']
route2 = os.environ['ROUTE2']
secret = os.environ['SECRET_KEY']

app = Flask(__name__)
app.secret_key = secret


@app.route('/')
def index():
    getban = get('http://127.0.0.1:5000/fail2ban/getban').json()
    status = get('http://127.0.0.1:5000/fail2ban/status').json()
    return render_template(
        'index.html', getban=getban['result'], status=status['result']
        )


@app.route('/fail2ban/status')
def get_status():
    command = ['ssh', f'root@{host}', 'fail2ban-client', 'status']
    process = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="UTF-8"
        )
    return jsonify(result=process.stdout)


@app.route('/fail2ban/getban')
def get_ban():
    command = ['ssh', f'root@{host}', f'''for i in `route -n | cut -d' ' -f1`;
                do if [[ $i != {route1} && $i != {route2}
                && $i != 'Kernel' && $i != 'Destination' ]]; then
                echo $i; fi; done''']
    process = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding='UTF-8'
        )
    return jsonify(result=process.stdout)


@app.route('/fail2ban/ban', methods=['POST'])
def add_ban():
    command = ['ssh', f'root@{host}', 'fail2ban-client', 'set', 'zimbra-smtp',
               'banip', request.form.get('ipAddress')]
    process = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
        )
    if process.returncode == 0:
        flash('command success')
    else:
        flash('command error')
    return redirect(url_for('index'))


@app.route('/fail2ban/unban', methods=['POST'])
def remove_ban():
    command = ['ssh', f'root@{host}', 'fail2ban-client',
               'unban', request.form.get('ipAddress')]
    process = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
        )
    if process.returncode == 0:
        flash('command success')
    else:
        flash('command error')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
