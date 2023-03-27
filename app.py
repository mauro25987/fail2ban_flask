from flask import (
    Flask, jsonify, render_template, request, redirect, url_for, flash
)
from requests import get
import subprocess

app = Flask(__name__)

app.secret_key = (
    'dd9bf2b39ac8f99fc994fe8db39d1e5aa8d974f48f093defc7aed0f0d114c296'
)


@app.route('/')
def index():
    getban = get('http://127.0.0.1:5000/fail2ban/getban').json()
    status = get('http://127.0.0.1:5000/fail2ban/status').json()
    return render_template(
        'index.html', getban=getban['result'], status=status['result']
        )


@app.route('/fail2ban/status')
def get_status():
    command = ['fail2ban-client', 'status']
    process = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="UTF-8"
        )
    return jsonify(result=process.stdout)


@app.route('/fail2ban/getban')
def get_ban():
    command = ['sqlite3', '/var/lib/fail2ban/fail2ban.sqlite3',
               'select ip, jail from bips']
    process = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding='UTF-8'
        )
    return jsonify(result=process.stdout)


@app.route('/fail2ban/ban', methods=['POST'])
def add_ban():
    command = ['fail2ban-client', 'set', 'sshd',
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
    command = ['fail2ban-client', 'unban', request.form.get('ipAddress')]
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
    app.run(debug=True)
