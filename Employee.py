class Employee():
    def __init__(self, first_name, last_name, email):
        """Initialize instance of Employee class with name, age, and email properties"""
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def get_dict(self):
        """Return employee object in the form of a dictionary"""
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
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
