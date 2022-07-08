import datetime

from flask import Flask, render_template, url_for, request, redirect
from markupsafe import escape
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

import room_db
import user_db
from datetime import date
from random import randint



selected_room = None
final_date = None
username = None

app = Flask(__name__)
CORS(app)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:brunosql@localhost/reservita'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Horarios(db.Model):
    __tablename__ = 'horarios'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20))
    room = db.Column(db.String(200))
    intervalo = db.Column(db.String(200))
    aluno = db.Column(db.String(200))

    def __init__(self, date, room, intervalo, aluno):
        self.id = randint(1, 1000000)
        self.date = date
        self.room = room
        self.intervalo = intervalo
        self.aluno = aluno

class User(db.Model):
    __tablename__ = 'usuarios'
    username = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(200))
    def __init(self, name, password):
        self.username = name
        self.password = password

def valid_login(username, password): # checa se usuário apresentou credenciais válidas
    #return True
    return db.session.query(User).filter(User.username == username).filter(User.password == password).count() != 0
def check_schedule(room, date): # checa horários livres de uma sala
    #room ex: "A - Churrasqueira"
    #date ex: "8/7/2022"
    horarios_livres = ["00:00 - 00:30", "00:30 - 01:00", "01:00 - 01:30", "01:30 - 02:00", "02:00 - 02:30", "02:30 - 03:00", "03:00 - 03:30", "03:30 - 04:00", "04:00 - 04:30", "04:30 - 05:00", "05:00 - 05:30", "05:30 - 06:00", "06:00 - 06:30", "06:30 - 07:00","07:00 - 07:30", "07:30 - 08:00", "08:00 - 08:30", "08:30 - 09:00", "09:00 - 09:30", "09:30 - 10:00", "10:00 - 10:30", "10:30 - 11:00", "11:00 - 11:30", "11:30 - 12:00", "12:00 - 12:30", "12:30 - 13:00", "13:00 - 13:30", "13:30 - 14:00", "14:00 - 14:30", "14:30 - 15:00", "15:00 - 15:30", "15:30 - 16:00", "16:00 - 16:30", "16:30 - 17:00", "17:00 - 17:30", "17:30 - 18:00", "18:00 - 18:30", "18:30 - 19:00", "19:00 - 19:30", "19:30 - 20:00", "20:00 - 20:30", "20:30 - 21:00", "21:00 - 21:30", "21:30 - 22:00", "22:00 - 22:30", "22:30 - 23:00", "23:00 - 23:30", "23:30 - 24:00"]
    for horario in horarios_livres:
        if db.session.query(Horarios).filter(Horarios.intervalo == horario).filter(Horarios.room == room).filter(Horarios.date == date).count() != 0:
            horarios_livres.remove(horario)
    return horarios_livres # returns free schedule


def make_reservation(room, date, time, user): # faz reserva de uma sala para usuário na data solicitada
    print(date)
    reservation = Horarios(date, room, time, user)
    db.session.add(reservation)
    db.session.commit()


def cancel_reservation(room, date, time): # cancela a reserva do usuário
    pass

def check_past_reservations(room, user): # retorna todos as reservas feitas pelo user na sala room
    #if db.session.query(Horarios).filter(Horarios.room == room.filter(Horarios.aluno == user).count != 0:
    return [["10/7/2022", "14:00 - 14:30"], ["10/7/2022", "14:30 - 15:00"]]

@app.route('/')
def index():
    return redirect('/form')

@app.route('/form') #página de login
def form():
    return render_template('form.html')

@app.route('/data', methods=['POST', 'GET']) # página em que usário seleciona sala desejada ou escolhe viusalizar suas reservas anteriores
def data():
    if request.method == 'POST':
        form_data = request.form
        global username
        username = form_data['username']
        if valid_login(form_data['username'],form_data['password']):
            return render_template('choose_room_form.html', form_data=form_data)
        else:
            return render_template('wrong_login.html')
    else:
        return render_template('form.html')

@app.route('/choose_room_check', methods=['POST', 'GET']) # página em que o usuário escolhe a sala para então visualizar suas reservas ativas
def choose_room_check():
    error = None
    if request.method == 'POST':
        return render_template('choose_room_check_reservations.html')
    else:
        return render_template('form.html', error=error)


@app.route('/choose_date', methods=['POST', 'GET']) # página em que o usuário escolhe a data que quer reservar a sala
def choose_date():
    error = None
    if request.method == 'POST':
        form_data = request.form
        global selected_room
        selected_room = form_data["pergunta"]
        return render_template('choose_date_form.html', form_data=form_data)
    else:
        return render_template('form.html', error=error)

@app.route('/select_time', methods=['POST', 'GET']) # página em que o usuário selecona o horário desejado para realizar a reserva
def select_time():
    error = None
    if request.method == 'POST':
        form_data = request.form
        shift = int(form_data["pergunta"])
        reservation_date = date.today() + datetime.timedelta(days = shift)
        global final_date
        final_date = str(reservation_date.day) + '/' + str(reservation_date.month) + '/' + str(reservation_date.year)
        available_schedule = check_schedule(selected_room, final_date)
        return render_template('choose_hour_form.html', chosen_date = final_date, room = selected_room, schedule = available_schedule)
    else:
        return render_template('form.html', error=error)


@app.route('/select_scheduled_time', methods=['POST', 'GET']) # página em que o usuário seleciona os horários que deseja cancelar sua reserva
def select_scheduled_time():
    if request.method == 'POST':
        form_data = request.form
        global selected_room
        selected_room = form_data["pergunta"]
        past_reservations = check_past_reservations(selected_room, username)
        return render_template('select_scheduled_time.html', room = selected_room, schedule = [x + "->" + y for x,y in past_reservations])
    else:
        return render_template('form.html', error=error)


@app.route('/reservation_complete', methods=['POST', 'GET']) # página de redirecionamento para quando a reserva é feita com sucesso
def reservation_complete():
    error = None
    if request.method == 'POST':
        form_data = request.form
        for (x,time) in form_data.items():
            minute = int(time[3:5])
            hour = int(time[0:2])
            new_hour = str(hour)
            new_minute = str(minute)
            if(minute == 0 and hour < 10):
                new_hour = '0'+ str(hour)
                new_minute = '30'
            elif (minute == 0 and hour >=10):
                new_hour = str(hour)
                new_minute = '30'
            elif (minute == 30 and hour < 9):
                new_hour = '0' + str(hour+1)
                new_minute = '00'
            elif (minute == 30 and hour >= 9):
                new_hour = str(hour+1)
                new_minute = '00'
            make_reservation(selected_room, final_date, time + " - " + new_hour + ':' + new_minute, username)

        return render_template('reservation_complete.html')
    else:
        return render_template('form.html', error=error)


@app.route('/reservation_cancelled', methods=['POST', 'GET']) # página de redirecionamento para quando a reserva é cancelada com sucesso
def reservation_cancelled():
    error = None
    if request.method == 'POST':
        form_data = request.form
        for (x,txt) in form_data.items():
            temp = txt.split('->')
            time = temp[1]
            date = temp[0]
            minute = int(time[3:5])
            hour = int(time[0:2])
            new_hour = str(hour)
            new_minute = str(minute)
            if(minute == 0 and hour < 10):
                new_hour = '0'+ str(hour)
                new_minute = '30'
            elif (minute == 0 and hour >=10):
                new_hour = str(hour)
                new_minute = '30'
            elif (minute == 30 and hour < 9):
                new_hour = '0' + str(hour+1)
                new_minute = '00'
            elif (minute == 30 and hour >= 9):
                new_hour = str(hour+1)
                new_minute = '00'
            cancel_reservation(selected_room,  date, time + " - " + new_hour + ':' + new_minute)

        return render_template('reservation_complete.html')
    else:
        return render_template('form.html', error=error)

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5000)