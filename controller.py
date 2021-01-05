
from .database import *


class Controller:
    """ class to manage all the programm importing all the others classes"""
    def __init__(self):
        """Initialization"""
        self.appli = DataBase(user="root", password="Gab03nas18")

    def use_programm(self):
        exist = self.appli.db_exist()
        if not exist:
            self.appli.create_database()
            # .insert_data()
        else:
            self.appli.use_db()
