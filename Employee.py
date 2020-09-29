from setup import database
from setup import ObjectId
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

    def get_events(self):
        """Returns list of events for specific employee"""
        event_list = []
        for event_i in database.events.find({"employee": ObjectId(self.id)}):
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
            event_list.append(event.get_dict())
        self.events = event_list
        return event_list
