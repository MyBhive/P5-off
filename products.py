
class Product:
    """Class to handle a product object: to find, to parse or to insert in database"""

    def __init__(self, name, nutriscore, store, url, id):
        """Initialize the attribute of the product class"""
        # lecture des donnees
        self.name = name
        self.nutri = nutriscore
        self.store = store
        self.url = url
        self.id = id


    def select_products(self, mycursor, wish_cat):
        """Method to find the information about a certain amount of product"""
        query = "SELECT EXISTS (SELECT * FROM product where id_category = %s)"
        var = wish_cat
        mycursor.execute(query, var)
        data = mycursor.fetchall()
        return data

    def parsing_product(self, prod_base):
        """Method to find the information about a certain amount of product"""
        num_product = 0
        for e in prod_base:
            if num_product <= 10:
                print(num_product)
                print("Nom du produit: ", e[self.name])
                print("Nutriscore associé: ", e[self.nutri])
                print("magasin: ", e[self.store])
                print("Lien internet:", e[self.url])
                print(".........................")
                num_product += 1

    def insert_prod(self, mycursor, mysql, data):
        """Method to insert a new product inside the product database"""
        query = "INSERT INTO product (" \
                "name, " \
                "nutriscore, " \
                "store, " \
                "url, " \
                "id_category" \
                ") " \
                "VALUES (%s, %s, %s, %s, %s)"
        var = data
        mycursor.execute(query, var)
        mysql.commit()

    def api_db(self, prod_base, amount):
        """Method to find the information about a certain amount of product"""
        product_info = []
        num_product = 0
        for e in prod_base:
            if num_product <= amount:
                product_info.append(e[self.name])
                product_info.append(e[self.nutri])
                product_info.append(e[self.store])
                product_info.append(e[self.url])
                num_product += 1
