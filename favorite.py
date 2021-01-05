

class Favorite:
    """Class to handle a favorite object: to find, to parse or to insert in database"""

    def __init__(self, favorite_id, product_ref):
        """Initialize the attribute of the product class"""
        # lecture des donnees
        self.favorite_id = favorite_id
        self.product_ref = product_ref
        # recherche de donnees

    def find_favorite(self, mycursor, id):
        """Method to find the categories"""
        query = "SELECT EXISTS (select * from favorite where product_id= %s)"
        var = id
        mycursor.execute(query, var)
        data = mycursor.fetchall()
        return data

    def show_favorite(self, prod_selection):
        """Method to find the information about a certain amount of product"""
        num_product = 0
        for e in prod_selection:
            if num_product <= 10:
                print(num_product)
                print("produit n°: ", e[self.favorite_id])
                print("référence n°: ", e[self.product_ref])
                print(".........................")
                num_product += 1
