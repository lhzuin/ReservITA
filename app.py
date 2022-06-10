from flask import Flask, render_template, url_for, request, redirect
from markupsafe import escape
from flask_cors import CORS
import user_db
#from choose_room_form import pergunta
app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return redirect('/form')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/data', methods=['POST', 'GET'])
def data():
    error = None
    if request.method == 'POST':
        form_data = request.form
        if user_db.valid_login(form_data['username'],form_data['password']):
            return render_template('choose_room_form.html', form_data=form_data)
        else:
            error = 'Invalid username/password'
    else:
        return render_template('form.html', error=error)
    # the code below is executed if the request method
    # was GET or the credentials were invalid


@app.route('/choose_date', methods=['POST', 'GET'])
def choose_date():
    error = None
    if request.method == 'POST':
        form_data = request.form
        return render_template('choose_date_form.html', form_data=form_data)
    else:
        return render_template('form.html', error=error)
    # the code below is executed if the request method
    # was GET or the credentials were invalid

@app.route('/user/<username>/') #por enquanto é inútil
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'

@app.route('/select_room')
def select_room(username):
    #redirect('/select_room')
    return render_template('choose_room_form.html')

with app.test_request_context():
    print(url_for('index'))
    print(url_for('form'))
    print(url_for('show_user_profile', username='Zuin'))

def check():
    q1 = pergunta.value
    print(q1)


if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5000)