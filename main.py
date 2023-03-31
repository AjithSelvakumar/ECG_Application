import os
from flask import Flask, render_template, request, redirect, url_for, send_file

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'doctor' and password == '1234':
            print('Redirecting to /protected...')
            return redirect('/protected?username=' + username)
        else:
            print('Invalid username or password')
            return render_template('login.html', error='Invalid username or password')
    else:
        print('Rendering login page')
        return render_template('login.html')

@app.route('/protected', methods=['GET', 'POST'])
def protected():
    username = request.args.get('username')
    if username == 'doctor':
        print('Rendering protected page')
        if request.method == 'POST':
            action = request.form['action']
            if action == 'download':
                file_path = os.path.join(app.root_path, 'static', 'ecg.jpg')
                return send_file(file_path, as_attachment=True)
            elif action == 'view':
                view_url = url_for('static', filename='ecg.jpg')
                return render_template('protected.html', username=username, view=view_url)
        return render_template('protected.html', username=username)
    else:
        print('Redirecting to /login...')
        return redirect('/login')

@app.route('/download')
def download():
    file_path = os.path.join(app.root_path, 'static', 'ecg.jpg')
    return send_file(file_path, as_attachment=True)

@app.route('/view')
def view():
    view_url = url_for('static', filename='ecg.jpg')
    return render_template('protected.html', view=view_url)

if __name__ == '__main__':
    app.run(debug=True)
