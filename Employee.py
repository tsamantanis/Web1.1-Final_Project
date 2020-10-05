from setup import database
from setup import ObjectId
from datetime import date

from Event import Event

class Employee():
    def __init__(self, first_name, last_name, email):
        """Initialize instance of Employee class with name, age, and email properties"""
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.events = []

    def get_dict(self):
        """Return employee object in the form of a dictionary"""
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "events": self.events
        }

    def set_id(self, id):
        """Adds an id property to the Employee class to store MongoDb ObjectId"""
        self.id = id

    def update(self, first_name, last_name, email):
        """Updates employee details"""
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        database.employees.update_one({"_id": ObjectId(self.id)}, { "$set": get_dict() })

    def delete(self):
        """Overrise abstract method delete"""
        database.employees.delete_one({"_id": ObjectId(self.id)})

    def get_events_today(self):
        """Returns list of today's events for specific employee"""
        event_list = []
        timeslot_events = {
            "09:00-11:00": "",
            "11:00-13:00": "",
            "13:00-15:00": "",
            "15:00-17:00": ""
        }
        for event_i in database.events.find({"employee": ObjectId(self.id), "date": str(date.today())}):
            id = event_i['_id']
            event = Event(
                event_i['title'],
                event_i['employee'],
                event_i['color'],
                event_i['details'],
                event_i['date'],
                event_i['timeslot']
            )
            event.set_id(str(id))
            timeslot_events[event.timeslot] = event
            event_list.append(event.get_dict())
        self.events = timeslot_events
        return timeslot_events

    def get_events(self, date_input):
        """Returns list of events for specific employee on given date"""
        date_input = date(int(date_input[0:4]), int(date_input[5:7]), int(date_input[8:10]))
        event_list = []
        timeslot_events = {
            "09:00-11:00": "",
            "11:00-13:00": "",
            "13:00-15:00": "",
            "15:00-17:00": ""
        }
        for event_i in database.events.find({"employee": ObjectId(self.id), "date": str(date_input)}):
            id = event_i['_id']
            event = Event(
                event_i['title'],
                event_i['employee'],
                event_i['color'],
                event_i['details'],
                event_i['date'],
                event_i['timeslot']
            )
            event.set_id(str(id))
            timeslot_events[event.timeslot] = event
            event_list.append(event.get_dict())
        self.events = timeslot_events
        return timeslot_events
