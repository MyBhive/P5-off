import requests
import mysql.connector


class Product:
    """Class to create product's object
    and method to insert them inside a database"""

    def __init__(self, num_prod, category):
        """Initialize the attribute of the product class"""
        self.cnx = mysql.connector.connect(user='root',
                                           password='Gab03nas18',
                                           host='localhost')

        self.mycursor = self.cnx.cursor()
        self.response = requests.get("https://be-fr.openfoodfacts.org/cgi/"
                                     "search.pl?search_simple=1&"
                                     "action=process&"
                                     "tagtype_0=categories&"
                                     "tag_contains_0=contains&"
                                     "tag_0=pizza&"
                                     "sort_by=ciqual_food_name_tags&"
                                     "page_size=200&json=1")
        # lecture des donnees
        self.package = self.response.json()
        self.prod_base = self.package['products']
        self.prod_name = self.prod_base[num_prod]['product_name']
        self.brand = self.prod_base[num_prod]['brands']
        self.nutri = self.prod_base[num_prod]['nutrition_grades']
        self.store = self.prod_base[num_prod]['stores']
        self.url = self.prod_base[num_prod]['url']
        self.product_info = (
            self.prod_name,
            self.brand,
            self.nutri,
            self.store,
            self.url,
            category  # lien entre les bases donnees category et product
        )

        # recherche de donnees
    def find_data(self):
        """Method to find the information about a certain amount of product"""
        num_product = 0
        for e in self.prod_base:
            if num_product <= 20:
                print("Nom du produit: ", e[self.prod_name])
                print("Nutriscore associé: ", e[self.nutri])
                print("Lien internet:", e[self.url])
                print(".........................")
                num_product += 1

    def insert_into_base(self):
        """Method to insert a new product inside the product database"""
        query = "INSERT INTO product (" \
                "name, " \
                "brand, " \
                "nutriscore, " \
                "store, " \
                "url, " \
                "id_category" \
                ") " \
                "VALUES (%s, %s, %s, %s, %s, %s)"
        var = self.product_info
        self.mycursor.execute(query, var)
        self.cnx.commit()
