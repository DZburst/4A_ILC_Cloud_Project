import codecs
import sys
from urllib.parse import quote, unquote
from flask import Flask, abort, jsonify, request, url_for
from markupsafe import escape
from datetime import datetime
import json
import csv

app = Flask(__name__)

# Code from the previous project : 

"""

## Class representing the Events in the calendar.

class Event:
    name = None
    timestamp = None
    duration = None
    participants = None

    def __init__(self, name, timestamp, duration, participants):
        self.name = name
        self.timestamp = timestamp
        self.duration = duration
        self.participants = participants

test_event = Event("Holidays", "12/23/2023", 1382400, ["Everyone"])

calendars = {}
cal = {test_event.name : (test_event.timestamp, test_event.duration, test_event.participants)}
calendars["Default Calendar"] = cal

def value(x):
    return unquote(unquote(x))

@app.route('/')
def main_menu():
    current_url = request.headers.get('X-Forwarded-Proto', 'http') + '://' + request.headers.get('X-Forwarded-Host', 'localhost')
    if current_url.endswith('/'):
        current_url = current_url[:-1]
    text = "<h2 style = 'text-align : center;'>This is the main page of our project, at the root of the other endpoints. Please choose amongst the following endpoints. </h2><p style = 'text-align : center;'>(Beware when changing the values of T1 and n in the url, keep %25252F for '/' and %252520 for ' ', only change the values)</p> <br>"
    
    # Since the application to implement shouldn't have too many endpoints, we can add manually 
    # the default values for endpoints which require parameters.
    # Otherwise, we should create a list and get all the endpoints, access their properties with their rules,
    # and then do the necessary operations.

    #E1
    text += "<p><a href='{}{}'>/{}</a></p><br>".format(current_url, url_for('calendar', cal_name = quote('Default%20Calendar')), 'calendar')
    text += "<p><a href='{}{}'>/{}</a></p><br>".format(current_url, url_for('add_event', n = quote('Day%201'), T1 = quote('01%2F01%2F1970'), t = 86400, p = 'Everyone', cal_name = quote('Default%20Calendar')), 'add_event')
    text += "<p><a href='{}{}'>/{}</a></p><br>".format(current_url, url_for('remove_event', n = quote('Day%201'), cal_name = quote('Default%20Calendar')), 'remove_event')

    #E2
    text += "<p><a href='{}{}'>/{}</a></p><br>".format(current_url, url_for('sorted_events', cal_name = quote('Default%20Calendar')), 'sorted_events')
    
    #E3
    text += "<p><a href='{}{}'>/{}</a></p><br>".format(current_url, url_for('sorted_events_by_person', p = 'Everyone', cal_name = quote('Default%20Calendar')), 'sorted_events_by_person')

    #E4
    text += "<p><a href='{}{}'>/{}</a></p><br>".format(current_url, url_for('add_participant',n = quote('Day%201'), p = 'Someone', cal_name = quote('Default%20Calendar')), 'add_participant')

    #E5
    text += "<p><a href='{}{}'>/{}</a></p><br>".format(current_url, url_for('next_event', cal_name = quote('Default%20Calendar')), 'next_event')

    #E6
    text += "<p><a href='{}{}'>/{}</a></p><br>".format(current_url, url_for('export_csv', path = quote('Ressources%2FCI_CD_Project.csv'), cal_name = quote('Default%20CSV%20Calendar')), 'export_csv')

    return text

@app.route('/viewCalendar/<cal_name>', methods = ["GET"])
def calendar(cal_name):
    return jsonify(calendars[value(cal_name)])

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


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "check_syntax":
            print("Build OK")
            exit(0)
        else:
            print("Passed argument not supported ! Supported arguments : check_syntax")
            exit(1)

    app.run(debug = True)

"""