def check_schedule(room, date):
    #room ex: "A - Churrasqueira"
    #date ex: "08/07/2022"
    return ["00:00 - 00:30", "00:30 - 01:00", "01:00 - 01:30", "01:30 - 02:00", "07:00 - 07:30", "07:30 - 08:00"] # returns free schedule

def make_reservation(room, date, time, user):
    # time ex: "00:30 - 01:00"
    pass

def check_reservations(room, user):
    pass
class Room:
    def __init__(self, name, schedule_matrix):
        self.name = name
        self.schedule_matrix = schedule_matrix


def cancel_reservation(room, date, time):
    pass

def check_past_reservations(room, user): # retorna todos as reservas feitas pelo user na sala room conforme o formato abaixo
    return ["14:00 - 14:30  10/7/2022", "14:30 - 15:00  10/7/2022"]