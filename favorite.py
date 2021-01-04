

class Favorite:
    """Class to handle a favorite object: to find, to parse or to insert in database"""

    def __init__(self, prod_id, prod_code):
        """Initialize the attribute of the product class"""
        # lecture des donnees
        self.prod_id = prod_id
        self.prod_code = prod_code
        # recherche de donnees

    def find_data(self, mycursor):
        """Method to find the categories"""
        query = "SELECT EXISTS (select * from favorite where product_id= %s and fk_products_code= %s)"
        var = (self.prod_id, self.prod_code)
        mycursor.execute(query, var)
        data = mycursor.fetchall()
        return data

    def parsing(self, prod_selection):
        """Method to find the information about a certain amount of product"""
        num_product = 0
        for e in prod_selection:
            if num_product <= 10:
                print(num_product)
                print("produit n°: ", e[self.prod_id])
                print("référence n°: ", e[self.prod_code])
                print(".........................")
                num_product += 1
