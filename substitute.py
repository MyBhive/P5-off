

class Substitute:
    """Class to handle a favorite object: to find, to parse or to insert in database"""

    def __init__(self, substitute_id, product_ref):
        """Initialize the attribute of the product class"""
        # lecture des donnees
        self.substitute_id = substitute_id
        self.product_ref = product_ref
        # recherche de donnees

    def find_substitute(self, mycursor, id):
        """Method to find the categories"""
        query = "SELECT EXISTS (select * from favorite where product_id= %s)"
        var = id
        mycursor.execute(query, var)
        data = mycursor.fetchall()
        return data

    def show_substitute(self, prod_selection):
        """Method to find the information about a certain amount of product"""
        num_product = 0
        for e in prod_selection:
            if num_product <= 10:
                print(num_product)
                print("produit n°: ", e[self.substitute_id])
                print("référence n°: ", e[self.product_ref])
                print(".........................")
                num_product += 1

    def get_substitute(self, mycursor, id_category, nutriscore):
        """Method to choose a better nutriscore
        from a product in the category chosen"""
        query = "SELECT * FROM product " \
                "where id_category = %s " \
                "and nutri < %s ORDER by nutri"
        var = (id_category, nutriscore)
        answer = mycursor.execute(query, var)
        return answer

    def select_substitute(self, mycursor):
        """Method to join the product and the substitute Table
        to get all the datta from a substitute product"""
        query = "SELECT name, nutri, stores, url FROM product JOIN substitute ON product.id = substitute.product_id"
        mycursor.execute(query)
        data = mycursor.fetchall()
        return data

    def insert_into_substitute(self, mycursor, mysql, substitute_id):
        """Method to insert into the substitute Table a new substitute aliment"""
        query = "INSERT INTO substitute (substitute_id) VALUES (%s)"
        var = substitute_id
        mycursor.execute(query, var)
        mysql.commit()