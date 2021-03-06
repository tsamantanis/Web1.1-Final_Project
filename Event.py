from setup import ObjectId
from DB_Entity import DB_Entity
class Event(DB_Entity):
    def __init__(self, title, employee, color, details, date, timeslot):
        """Initialize instance of Event class with title, employee, color, details, and timeslot properties"""
        self.title = title
        self.employee = employee
        self.color = color
        self.details = details
        self.date = date
        self.timeslot = timeslot

    def get_dict(self):
        """Override abstract method get_dict"""
        employee_id = self.employee
        return {
            # "id": self.id,
            "title": self.title,
            "employee": ObjectId(employee_id),
            "color": self.color,
            "details": self.details,
            "date": self.date,
            "timeslot": self.timeslot
        }

    def update(self, title, employee, color, details, date, timeslot):
        """Override abstract method update"""
        self.title = title
        self.employee = employee
        self.color = color
        self.details = details
        self.date = date
        self.timeslot = timeslot
        database.events.update_one({"_id": ObjectId(self.id)}, { "$set": get_dict() })

    def delete(self):
        """Overrise abstract method delete"""
        database.events.delete_one({"_id": ObjectId(self.id)})
