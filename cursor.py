import mysql.connector
import requests
import pdb
pdb.set_trace()


""" constant data for the purebeurre application"""
CATEGORY = {
    1: "snacks",
    2: "pizzas",
    3: "dessert",
    4: "charcuteries",
    5: "boissons"
}


class Category:
    """Class to handle a category object: to find,
    to parse or to insert in database"""
    def __init__(self, id, name):
        """Initialize the attribute of the category class"""
        self.id = id
        self.name = name
        self.mysql = mysql.connector.connect(user="root",
                                             password="Gab03nas18",
                                             host='localhost')
        self.mycursor = self.mysql.cursor()

    def select_category(self):
        """Method to find the categories"""
        query = "SELECT EXISTS (SELECT * FROM category)"
        self.mycursor.execute(query)
        data = self.mycursor.fetchall()
        return data

    def parsing_category(self, prod_base):
        """Method of parsing the categories"""
        num_cat = 0
        for e in prod_base:
            if num_cat <= 10:
                print(num_cat)
                print("catégorie: ", e[self.name])
                print(".........................")
                num_cat += 1

    def insert_cat(self):
        """Method to insert a new category inside the category database"""
        query = "INSERT INTO category (id, name) " \
                "VALUES (%s, %s)"
        var = (self.name, self.id)
        self.mycursor.execute(query, var)
        self.mysql.commit()


class Product:
    """Class to handle a product object: to find,
    to parse or to insert in database"""

    def __init__(self, prod_base, num_product, category):
        """Initialize the attribute of the product class"""
        self.mysql = mysql.connector.connect(user="root",
                                             password="Gab03nas18",
                                             host='localhost')
        self.mycursor = self.mysql.cursor()
        # lecture des donnees
        self.name = prod_base[num_product]["product_name"]
        self.nutri = prod_base[num_product]["nutrition_grades"]
        self.store = prod_base[num_product]["stores"]
        self.url = prod_base[num_product]["url"]
        self.id = category
        self.product_info = []

    def select_products(self, wish_cat):
        """Method to find the information
        about a certain amount of product"""
        query = "SELECT EXISTS " \
                "(SELECT * FROM product " \
                "WHERE id_category = %s)"
        var = wish_cat
        self.mycursor.execute(query, var)
        data = self.mycursor.fetchall()
        return data

    def parsing_product(self, prod_base):
        """Method to find the information about a certain amount of product"""
        num_product = 0
        for e in prod_base:
            if num_product <= 10:
                print("___________________________________")
                print(self.id)
                print("Nom du produit: ", e[self.name])
                print("Nutriscore associé: ", e[self.nutri])
                print("magasin: ", e[self.store])
                print("Lien internet:", e[self.url])
                print("___________________________________")
                num_product += 1

    def insert_prod(self, data):
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
        self.mycursor.execute(query, var)
        self.mysql.commit()

    def api_db_list_create(self, prod_base, amount):
        """Method to find the information
        about a certain amount of product"""
        num_product = 0
        for e in prod_base:
            if num_product <= amount:
                self.product_info.append(e[self.name])
                self.product_info.append(e[self.nutri])
                self.product_info.append(e[self.store])
                self.product_info.append(e[self.url])
                num_product += 1

    def get_nutriscore(self, id):
        """Method to get the nutriscore from a product"""
        query = "SELECT EXISTS " \
                "(SELECT nutri FROM product " \
                "WHERE id = %s)"
        var = id
        answer = self.mycursor.execute(query, var)
        return answer


class Substitute:
    """Class to handle a substitute object: to find,
    to parse or to insert in database"""

    def __init__(self, substitute_id, product_ref):
        """Initialize the attribute of the product class"""
        # lecture des donnees
        self.substitute_id = substitute_id
        self.product_ref = product_ref
        self.mysql = mysql.connector.connect(user="root",
                                             password="Gab03nas18",
                                             host='localhost')
        self.mycursor = self.mysql.cursor()
        # recherche de donnees

    def find_substitute(self, id):
        """Method to find the categories"""
        query = "SELECT EXISTS " \
                "(SELECT * FROM substitute " \
                "WHERE product_id= %s)"
        var = id
        self.mycursor.execute(query, var)
        data = self.mycursor.fetchall()
        return data

    def show_substitute(self, prod_selection):
        """Method to find the information
        about a certain amount of product"""
        self.mysql = mysql.connector.connect(user="root",
                                             password="Gab03nas18",
                                             host='localhost')
        self.mycursor = self.mysql.cursor()
        num_product = 0
        for e in prod_selection:
            if num_product <= 10:
                print("produit n°: ", e[self.substitute_id])
                print("référence n°: ", e[self.product_ref])
                print(".........................")
                num_product += 1

    def get_substitute(self, id_category, nutriscore):
        """Method to choose a better nutriscore
        from a product in the category chosen"""
        query = "SELECT * FROM product " \
                "where id_category = %s " \
                "and nutri < %s ORDER by nutri"
        var = (id_category, nutriscore)
        answer = self.mycursor.execute(query, var)
        return answer

    def select_substitute(self):
        """Method to join the product and the substitute Table
        to get all the datta from a substitute product"""
        query = "SELECT name, nutri, stores, url " \
                "FROM product " \
                "JOIN substitute " \
                "ON product.id = substitute.product_id"
        self.mycursor.execute(query)
        data = self.mycursor.fetchall()
        for info in data:
            print("You have chosen {} has substitute".format(info[0]))
            print("the nutriscore is '{}'".format(info[1]))
            print("You can find it on this store: {}".format(info[2]))
            print("For more information, clic on the link: {}".format(info[3]))

    def insert_into_substitute(self, substitute_id):
        """Method to insert into the
        substitute Table a new substitute aliment"""
        query = "INSERT INTO substitute (substitute_id) " \
                "VALUES (%s)"
        var = substitute_id
        self.mycursor.execute(query, var)
        self.mysql.commit()

    def substitute_found(self):
        pass


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
        category, product and substitute"""
        opening = "CREATE DATABASE purbeurre CHARACTER SET 'utf8'"
        using = "USE purbeurre"
        # creating a table category :
        # the id is not auto increment to choose one per category
        # exemple : 1 for pizza, 2 for frozen, 3 for cakes etc
        table_category = "CREATE TABLE category " \
                         "(id SMALLINT NOT NULL, " \
                         "PRIMARY KEY(id)," \
                         "name VARCHAR(30)) " \
                         "ENGINE = INNODB"
        # creating a table product
        # to integrate the products and all their data
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
        # the substitute Table is simple
        # because it will be join to the product table later.
        # Better not to repeat informations
        table_substitute = "CREATE TABLE substitute " \
                           "(substitute_id SMALLINT " \
                           "NOT NULL AUTO_INCREMENT, " \
                           "PRIMARY KEY(substitute_id), " \
                           "product_ref SMALLINT  NOT NULL, " \
                           "CONSTRAINT fk_products_id " \
                           "FOREIGN KEY(product_ref) " \
                           "REFERENCES product(id)) " \
                           "ENGINE = INNODB"
        self.mycursor.execute(opening)
        self.mycursor.execute(using)
        self.mycursor.execute(table_category)
        self.mycursor.execute(table_product)
        self.mycursor.execute(table_substitute)
        self.mysql.commit()

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
            cat.insert_cat()
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
                num_product = 0
                product = Product(prod_base, num_product, key)
                try:
                    product.api_db_list_create(prod_base, 10)
                    list = product.product_info
                    for item in list:
                        # test and trigger an error if the condition is false.
                        assert len(str(item)) > 0
                        product.insert_prod(item)
                        print("the category " + CATEGORY[value] + "is valid")
                        max_products += 1
                # not the good dictionary key
                except KeyError:
                    pass
                # if the assert return False
                except AssertionError:
                    pass
                # if the function gets  improper value.
                except ValueError:
                    pass
                # if interpreter detects internal error.
                except SyntaxError:
                    pass

    def ask_category(self):
        print("___________________________________")
        print("Select the category of your choice: ")
        print("___________________________________")
        categories = CATEGORY
        for key, value in categories.items():
            print(key, "->", value)
            print("___________________________________")
        user_input = int(input("choice number: "))
        try:
            assert user_input
        except ValueError:
            print("please choose one of the proposed category's NUMBER")
        if 0 > user_input > 6:
            print("please choose one of the proposed category's number")

    def ask_product(self, list_product):
        print("___________________________________")
        print("Which product would you like to substitute?")
        print("___________________________________")
        print(list_product)
        user_input = int(input("choice number: "))
        try:
            assert user_input
        except ValueError:
            print("please choose one of the proposed category's NUMBER")
        if 0 > user_input > 11:
            print("please choose one of the proposed category's number")
            # suite à Product.parsing


class Controller:
    """ class to manage all the programm
    importing all the others classes"""
    def __init__(self):
        """Initialization"""
        self.appli = DataBase(user="root", password="Gab03nas18")
        self.cat = Category(CATEGORY[0], Category[1])

    def use_programm(self):
        exist = self.appli.db_exist()
        if exist:
            self.appli.use_db()
        else:
            self.appli.create_database()
            self.appli.insert_data(10)

        run = 1

        while run:
            question = input("To search a product and his substitute tape: 'O' "
                             "To search your substitute selection tape: 'Y', "
                             "TO quite the program tape: 'Q' ")
            if question == "O":
                self.cat.select_category()
                self.cat.parsing_category(prod_base="")





