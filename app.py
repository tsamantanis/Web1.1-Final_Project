from flask import request, redirect, render_template, url_for
import json
# from flask_pymongo import PyMongo
# from bson.objectid import ObjectId
from setup import app
from setup import database
from setup import ObjectId
from datetime import date, datetime, timedelta
import calendar

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
    context = {
        'employees': database.employees.find(),
        'events': database.events.find()
    }
    return render_template('home.html', **context)

@app.route('/get_calendar/<date_input>')
def get_calendar(date_input):
    """Returns current state of the calendar"""
    employees = database.employees.find()
    employee_list = []
    for employee in employees:
        a_employee = Employee(employee['first_name'], employee['last_name'], employee['email'])
        id = employee['_id']
        a_employee.set_id(str(id))
        a_employee.get_events(date_input)
        employee_list.append(a_employee)
    month_range = calendar.monthrange(int(date_input[0:4]), int(date_input[5:7]))
    prev_month_range = calendar.monthrange(int(date_input[0:4]), int(date_input[5:7]) - 1)
    date_current = date(int(date_input[0:4]), int(date_input[5:7]), int(date_input[8:10]))
    date_next = date(int(date_input[0:4]), int(date_input[5:7]), int(date_input[8:10]) + 1 if int(date_input[8:10]) < month_range[1] else 1)
    date_prev = date(int(date_input[0:4]), int(date_input[5:7]), int(date_input[8:10]) - 1 if int(date_input[8:10]) > 1 else prev_month_range[1])
    context = {
        "timeslots": timeslots,
        "employee_list": employee_list,
        "date": str(date_current.month) + "/" + str(date_current.day),
        "date_full": date_input,
        "date_next": date_next.strftime('%Y-%m-%d'),
        "date_prev": date_prev.strftime('%Y-%m-%d')
    }
    return render_template('calendar.html', **context)

@app.route('/new_event/<employee_id>/<date_input>/<timeslot>', methods=['GET', 'POST'])
def new_event(employee_id, date_input, timeslot):
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
            "employee_id": ObjectId(employee_id),
            "timeslot_input": timeslot,
            "date_input": date_input,
            "employees": database.employees.find(),
            "timeslots": timeslots,
            "min_date": datetime.now(),
            'max_date': datetime.now() + timedelta(days=25),
        }
        return render_template('new_event.html', **context)


@app.route('/new_employee', methods=['GET', 'POST'])
def new_employee():
    """Display the employee creation page & process data from the creation form."""
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
    """Display the event edit page."""
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
        context = {
            'event' : event_to_show,
            "employees": database.employees.find(),
            "timeslots": timeslots,
            "min_date": datetime.now(),
            'max_date': datetime.now() + timedelta(days=25),
        }
        return render_template('edit_event.html', **context)

@app.route('/edit_employee/<employee_id>', methods=['GET', 'POST'])
def edit_employee(employee_id):
    """Display the employee's edit page."""
    if request.method == 'POST':
        updated_employee_info = { "$set": {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email']
        }}

        res = database.employees.update_one({"_id": ObjectId(employee_id)}, updated_employee_info)
        new_employee.set_id(res.inserted_id)
        return redirect(url_for('get_calendar'))

    else:
        employee_to_show = database.employees.find_one_or_404({"_id": ObjectId(employee_id)})
        context = {
            'employee' : employee_to_show,
            'employee_id': employee_id
        }
        return render_template('edit_employee.html', **context)


@app.route('/delete_employee/<employee_id>')
def delete_employee(employee_id):
    """Delete's specified employee and all of their events"""
    database.events.delete_many({"employee": ObjectId(employee_id)})
    database.employees.delete_one({"_id": ObjectId(employee_id)})
    return redirect(url_for('get_calendar', date_input=datetime.now().strftime('%Y-%m-%d')))

@app.route('/delete_event/<event_id>')
def delete_event(event_id):
    """Delete's specified event"""
    database.events.delete_one({"_id": ObjectId(event_id)})
    return redirect(url_for('get_calendar', date_input=datetime.now().strftime('%Y-%m-%d')))

# Error Handling

@app.errorhandler(404)
def show_404(error):
    """Display a 404 error page"""
    return render_template('error_page.html', message = "This page has melted in the sun", button = "Back to Home"), 404

if __name__ == '__main__':
    app.run(debug=True)
