from flask import request, redirect, render_template, url_for
import json
# from flask_pymongo import PyMongo
# from bson.objectid import ObjectId
from setup import app
from setup import database
from setup import ObjectId
from datetime import date, datetime, timedelta

from timeslots import timeslots
from Event import Event
from Employee import Employee
from Calendar import Calendar

# app = Flask(__name__)
#
# app.config["MONGO_URI"] = "mongodb://localhost:27017/kanbanCalendar"
# mongo = PyMongo(app)
# database = mongo.db

@app.route('/')
def home():
    """Display all events and employees in kanban calendar."""
    print(date.today())
    context = {
        'employees': database.employees.find(),
        'events': database.events.find()
    }
    return render_template('home.html', **context)

@app.route('/get_calendar')
def get_calendar():
    """Returns current state of the calendar"""
    employees = database.employees.find()
    employee_list = []
    for employee in employees:
        a_employee = Employee(employee['first_name'], employee['last_name'], employee['email'])
        id = employee['_id']
        a_employee.set_id(str(id))
        a_employee.get_events_today()
        employee_list.append(a_employee)
    # calendar = Calendar(employee_list)
    # print(calendar.get_dict())
    # return json.dumps(calendar.get_dict())
    context = {
        "timeslots": timeslots,
        "employee_list": employee_list
    }
    return render_template('calendar.html', **context)

@app.route('/new_event', methods=['GET', 'POST'])
def new_event():
    """Display the event creation page & process data from the creation form."""
    if request.method == 'POST':
        new_event = Event(
            request.form['title'],
            ObjectId(request.form['employee']),
            request.form['color'],
            request.form['details'],
            request.form['date'],
            request.form['timeslot']
        )

        res = database.events.insert_one(new_event.get_dict())
        new_event.set_id(res.inserted_id)
        return redirect(url_for('home'))

    else:
        context = {
            "employees": database.employees.find(),
            "timeslots": timeslots,
            "min_date": datetime.now(),
            'max_date': datetime.now() + timedelta(days=25),
        }
        return render_template('new_event.html', **context)


@app.route('/new_employee', methods=['GET', 'POST'])
def new_employee():
    """Display the event creation page & process data from the creation form."""
    if request.method == 'POST':
        new_employee = Employee(
            request.form['first_name'],
            request.form['last_name'],
            request.form['email']
        )

        res = database.employees.insert_one(new_employee.get_dict())
        new_employee.set_id(res.inserted_id)
        return redirect(url_for('home'))

    else:
        return render_template('new_employee.html')

@app.route('/edit_event/<event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    """Display the event details page."""
    if request.method == 'POST':
        updated_event_info = { "$set": {
            'title': request.form["title"],
            'employee': ObjectId(request.form["employee"]),
            'color': request.form["color"],
            'details': request.form["details"],
            'date': request.form["date"],
            'timeslot': request.form["timeslot"],
        }}
        database.events.update_one({"_id": ObjectId(event_id)}, updated_event_info)
        return redirect(url_for('get_calendar'))
    else:
        event_to_show = database.events.find_one_or_404({"_id": ObjectId(event_id)})
        print(event_to_show['title'])
        context = {
            'event' : event_to_show,
            "employees": database.employees.find(),
            "timeslots": timeslots,
            "min_date": datetime.now(),
            'max_date': datetime.now() + timedelta(days=25),
        }
        return render_template('edit_event.html', **context)


@app.route('/delete/<event_id>')
def delete(event_id):
    """Delete's specified event and all of its harvest data"""
    database.events.delete_one({"_id": ObjectId(event_id)})
    return redirect(url_for('get_calendar'))

# Error Handling

@app.errorhandler(404)
def show_404(error):
    """Display a 404 error page"""
    return render_template('error_page.html', message = "This page has melted in the sun", button = "Back to Home"), 404

if __name__ == '__main__':
    app.run(debug=True)
