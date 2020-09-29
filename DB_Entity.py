from abc import ABC, abstractmethod
class DB_Entity(ABC):
    def set_id(self, id):
        """Adds an id property to the instance of database entity to store MongoDb ObjectId"""
        self.id = id

    @abstractmethod
    def get_dict(self):
        """Returns object in the form of a dictionary"""
        pass

    @abstractmethod
    def update(self):
        """Updates database entity details"""
        pass

    def delete(self):
        """Deletes database entity"""
        pass
