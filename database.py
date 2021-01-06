import mysql.connector
import requests

from .constant import *
from .category import *
from .products import *


class DataBase:
    """Class to enter and manipulate the database"""
    def __init__(self, user, password):
        """Initialize the attribute of the product class"""
        self.user = user
        self.password = password
        self.mysql = mysql.connector.connect(
            user=self.user,
            password=self.password,
            host='localhost')
        self.mycursor = self.mysql.cursor()

    def create_database(self):
        """Method to create a database with 3 tables:
        category, product and favorite"""
        opening = "CREATE DATABASE purbeurre CHARACTER SET 'utf8'"
        using = "USE purbeurre"
        # creating a table category : the id is not auto increment to choose one per category
        # exemple : 1 for pizza, 2 for frozen, 3 for cakes etc
        table_category = "CREATE TABLE category " \
                         "(id SMALLINT NOT NULL, " \
                         "PRIMARY KEY(id)," \
                         "name VARCHAR(30)) " \
                         "ENGINE = INNODB"
        # creating a table product to integrate the products and all their data
        # id, name, brand, nutriscore, stores, url and
        # id category and the foreign key to the table category
        table_product = "CREATE TABLE product " \
                        "(id SMALLINT  NOT NULL AUTO_INCREMENT," \
                        "PRIMARY KEY(id)," \
                        "name VARCHAR(50)," \
                        "nutri CHAR(1)," \
                        "stores VARCHAR (50)," \
                        "url VARCHAR(50)," \
                        "id_category SMALLINT NOT NULL," \
                        "CONSTRAINT fk_product_category " \
                        "FOREIGN KEY(id_category) " \
                        "REFERENCES category(id)) " \
                        "ENGINE = INNODB"
        table_favorite = "CREATE TABLE favorite " \
                         "(favorite_id SMALLINT NOT NULL AUTO_INCREMENT," \
                         "PRIMARY KEY(favorite_id)," \
                         "product_ref SMALLINT  NOT NULL, " \
                         "CONSTRAINT fk_products_id FOREIGN KEY(product_ref) " \
                         "REFERENCES product(id)) " \
                         "ENGINE = INNODB"
        self.mycursor.execute(opening)
        self.mycursor.execute(using)
        self.mycursor.execute(table_category)
        self.mycursor.execute(table_product)
        self.mycursor.execute(table_favorite)

    def db_exist(self):
        """Method to check if the database 'purbeurre' has been created"""
        info = []
        self.mycursor.execute("SHOW DATABASES LIKE 'purbeurre'")
        for data in self.mycursor:
            info.append(data)
        return info

    def use_db(self):
        """Method to open and use the database 'purbeurre'"""
        self.mycursor.execute("USE purbeurre")

    def insert_data(self, amount_wanted):
        """méthode qui va chercher les categories et
        produits sur l'api pour les enregistrer dans la db"""
        for key, value in CATEGORY.items():
            cat = Category(key, value)
            cat.insert_cat(self.mycursor, self.mysql)
            max_products = 0
            while max_products < amount_wanted:
                page = ("https://fr.openfoodfacts.org/cgi/"
                        "search.pl?search_simple=1&"
                        "action=process&"
                        "tagtype_0=categories&"
                        "tag_contains_0=contains&"
                        "tag_0={}&"
                        "sort_by=ciqual_food_name_tags&"
                        "page_size=200&json=1".format(value))
                response = requests.get(page)
                package = response.json()
                prod_base = package['products']
                product = Product('product_name', 'nutrition_grades', 'stores', 'url', key)
                data_list = product.api_db(prod_base, 10)
                for item in data_list:
                    product.insert_prod(self.mycursor, self.mysql, item)
