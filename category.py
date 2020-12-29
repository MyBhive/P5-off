
import mysql.connector


class Category:
    """Class to create categories
    and method to insert them inside a database"""

    def __init__(self, id, name):
        """Initialize the attribute of the category class"""
        self.cnx = mysql.connector.connect(user='root',
                                           password='Gab03nas18',
                                           host='localhost')

        self.mycursor = self.cnx.cursor()
        self.category = {
            1: "snacks",
            2: "pizzas",
            3: "dessert",
            4: "charcuteries",
            5: "boissons"
        }
        self.id = id
        self.name = name
        self.cate = (
            self.id,
            self.name
        )

    def insert_cat(self):
        """Method to insert a new category inside the category database"""
        query = "INSERT INTO category (id, name) VALUES (%s, %s)"
        var = self.cate
        self.mycursor.execute(query, var)
        self.cnx.commit()
