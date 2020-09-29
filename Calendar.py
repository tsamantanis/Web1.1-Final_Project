class Calendar():
    def __init__(self, employees):
        """Initialize instance of Calendar class"""
        self.employees = employees

    def get_dict(self):
        """Returns calendar in dictionary format"""
        return {
            "employees": [employee.get_dict() for employee in self.employees]
        }
