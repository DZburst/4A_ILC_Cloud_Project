import codecs
import sys
from urllib.parse import quote, unquote
from flask import Flask, abort, jsonify, request, url_for
from markupsafe import escape
from datetime import datetime
import json
import csv

app = Flask(__name__)

class Calcul:
    id = -1
    operand1 = 1
    operator = ""
    operand2 = 1

    def __init__(self, id, operand1, operator, operand2):
        Calcul.id += 1
        self.operand1 = operand1
        self.operator = operator
        self.operand2 = operand2
    
    def calculate(self):
        if self.operator == "+":
            return self.operand1 + self.operand2
        elif self.operator == "-":
            return self.operand1 - self.operand2
        elif self.operator == "*":
            return self.operand1 * self.operand2
        elif self.operator == "%2F":
            if self.operand2 != 0:
                return self.operand1 / self.operand2
            else:
                return "Error : Division by 0 impossible..."
        else:
            return "Error : Invalid operator"

test_calcul = Calcul(Calcul.id, 1, "+", 1)

operations = {}
result = test_calcul.operand1
operations[str(test_calcul.id)] = (test_calcul.operand1, test_calcul.operator, test_calcul.operand2, test_calcul.calculate())

def value(x):
    return unquote(unquote(x))

@app.route('/')
def main_menu():
    current_url = request.headers.get('X-Forwarded-Proto', 'http') + '://' + request.headers.get('X-Forwarded-Host', 'localhost')
    if current_url.endswith('/'):
        current_url = current_url[:-1]
    text = "<h2 style = 'text-align : center;'>To use the calculator, please type in the first operand, then the operator (\"+\", \"-\", \"*\", or \"%2F\" for division), then the second operand.</h2><br>"
    
    return text

@app.route('/viewCalculs', methods = ["GET"])
def viewCalculs():
    return jsonify(operations)


@app.route('/calculate/<operand1>/<operator>/<operand2>', methods = ["GET", "POST"])
def calculate(operand1, operator, operand2):
    new_calcul = Calcul(Calcul.id, int(operand1), value(operator), int(operand2))
    operations[str(new_calcul.id)] = (int(new_calcul.operand1), value(new_calcul.operator), int(new_calcul.operand2), new_calcul.calculate())
    return str(new_calcul.id)


@app.route('/viewCalculWithId/<id>', methods = ["GET"])
def viewCalculWithId(id):
    return jsonify(operations[str(id)])



# Code from the previous project : 

"""

@app.route('/addEvent/<n>/<T1>/<t>/<p>/<cal_name>', methods = ["GET", "POST"])
def add_event(n, T1, t, p, cal_name):
    new_event = Event(value(n), value(T1), int(value(t)), [value(p)])
    calendars[value(cal_name)][new_event.name] = (new_event.timestamp, new_event.duration, new_event.participants)
    return jsonify(calendars[value(cal_name)])

@app.route('/removeEvent/<n>/<cal_name>', methods = ["GET", "DELETE"])
def remove_event(n, cal_name):
    if value(n) in calendars[value(cal_name)]:
        calendars[value(cal_name)].pop(value(n))
    return jsonify(calendars[value(cal_name)])
    
@app.route('/sortEvents/<cal_name>', methods=["GET", "POST"])
def sorted_events(cal_name):
    sorted_cal = sorted(calendars[value(cal_name)].items(), key = lambda entry : datetime.strptime(entry[1][0], "%m/%d/%Y"))
    calendars[value(cal_name)].clear()
    for name, (timestamp, duration, participants) in sorted_cal:
        calendars[value(cal_name)][name] = (str(timestamp), duration, participants)

    return json.dumps(calendars[value(cal_name)], sort_keys = False)

@app.route('/sortedEventsByPerson/<p>/<cal_name>', methods=["GET"])
def sorted_events_by_person(p, cal_name):
    sorted_cal = sorted(calendars[value(cal_name)].items(), key = lambda entry : datetime.strptime(entry[1][0], "%m/%d/%Y"))
    p_sorted_cal = {}
    for name, (timestamp, duration, participants) in sorted_cal:
        if p in participants:
            p_sorted_cal[name] = (str(timestamp), duration, participants)
    calendars["{}'s sorted calendar".format(value(cal_name))] = p_sorted_cal
    
    return json.dumps(calendars["{}'s sorted calendar".format(value(cal_name))], sort_keys = False)

@app.route('/addParticipant/<n>/<p>/<cal_name>', methods=["GET", "POST"])
def add_participant(n, p, cal_name):
    if value(n) in calendars[value(cal_name)]:
        calendars[value(cal_name)][value(n)][2].append(value(p))
        return jsonify(calendars[value(cal_name)])
    else:
        return jsonify("No such event in {} ...".format(value(cal_name)))

@app.route('/viewCalendar/nextEvent/<cal_name>', methods=["GET"])
def next_event(cal_name):
    now = datetime.now().date()
    upcoming_events = []
    for name, (timestamp, time, participants) in calendars[value(cal_name)].items():
        if datetime.strptime(timestamp, "%m/%d/%Y").date() >= now:
            upcoming_events.append((name, timestamp, time, participants))

    next_event = min(upcoming_events, key = lambda x : datetime.strptime(x[1], "%m/%d/%Y"))
    formatted_event = {"Name" : next_event[0], "Timestamp" : next_event[1], "Duration" : next_event[2], "Participants" : next_event[3]}
    return jsonify(formatted_event)
    
@app.route('/exportCSV/<path>/<cal_name>', methods = ["GET", "POST"])
def export_csv(path, cal_name):
    entries = {}
    with codecs.open(value(path), 'r', 'utf-8-sig') as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            if 'Name' in row and 'Timestamp' in row and 'Duration' in row and 'Participants' in row:
                entries[row['Name']] = (row['Timestamp'], int(row['Duration']), row['Participants'])
    
    calendars[value(cal_name)] = entries
    
    return jsonify(calendars[value(cal_name)])

"""

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "check_syntax":
            print("Build OK")
            exit(0)
        else:
            print("Passed argument not supported ! Supported arguments : check_syntax")
            exit(1)

    app.run(debug = True)