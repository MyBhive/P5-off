

class Category:
    """Class to handle a category object: to find, to parse or to insert in database"""

    def __init__(self, id, name):
        """Initialize the attribute of the category class"""
        self.id = id
        self.name = name
        self.cate = (
            self.id,
            self.name
        )

    def find_data(self, mycursor):
        """Method to find the categories"""
        query = "SELECT EXISTS (select * from category where name= %s)"
        var = self.name
        mycursor.execute(query, var)
        data = mycursor.fetchall()
        return data

    def parsing(self, prod_base):
        """Method of parsing the categories"""
        num_cat = 0
        for e in prod_base:
            if num_cat <= 10:
                print(num_cat)
                print("catégorie: ", e[self.name])
                print(".........................")
                num_cat += 1

    def insert_cat(self, mycursor):
        """Method to insert a new category inside the category database"""
        query = "INSERT INTO category (id, name) VALUES (%s, %s)"
        var = self.cate
        mycursor.execute(query, var)
