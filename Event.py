class Event():
    def __init__(self, title, employee, color, details, date, timeslot):
        """Initialize instance of Event class with title, employee, color, details, and timeslot properties"""
        self.title = title
        self.employee = employee
        self.color = color
        self.details = details
        self.date = date
        self.timeslot = timeslot

    def set_id(self, id):
        """Adds an id property to the Event class to store MongoDb ObjectId"""
        self.id = id

    def get_dict(self):
        """Override abstract method"""
        return {
            "title": self.title,
            "employee": self.employee,
            "color": self.color,
            "details": self.details,
            "date": self.date,
            "timeslot": self.timeslot
        }

    def update(self, title, employee, color, details, date, timeslot):
        """Override abstract method"""
        self.title = title
        self.employee = employee
        self.color = color
        self.details = details
        self.date = date
        self.timeslot = timeslot
        database.events.update_one({"_id": ObjectId(self.id)}, { "$set": get_dict() })