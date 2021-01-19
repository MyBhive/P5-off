import mysql.connector
import requests
from random import choices
import yaml

"""constant data for the purbeurre application"""
CATEGORY = {
    1: "desserts-glaces",
    2: "pizzas",
    3: "chocolats",
    4: "soupes",
    5: "boissons",
    6: "biscuits",
    7: "viandes",
    8: "cereales",
    9: "pains",
    10: "yaourts"
}


class Category:
    """Class to handle a category object"""
    def __init__(self, id, name):
        """Initialize the attribute of the category class"""
        self.id = id
        self.name = name


class Product:
    """Class to handle a product object"""
    def __init__(self, name, nutri, store, url, category):
        """Initialize the attribute of the product class"""
        self.name = name
        self.nutri = nutri
        self.store = store
        self.url = url
        self.id = category


class Substitute:
    """Class to handle a substitute object"""
    def __init__(self, substitute_id, product_ref):
        """Initialize the attribute of the product class"""
        self.substitute_id = substitute_id
        self.product_ref = product_ref


class View:
    """Class to handle all the view for the program (print)"""
    def ask_category(self, list_category):
        """To ask the costumer to choose a category of product"""
        print("___________________________________")
        print("Select the category of your choice: ")
        print("___________________________________")
        for cat in list_category:
            print("Category N°: {}".format(cat[0]))
            print("Category Name: {}".format(cat[1]))
            print("___________________________________")
        try:
            user_input = int(input("number chosen: "))
            if 0 <= user_input <= 10:
                return user_input
            return self.ask_category(list_category)
        except ValueError:
            return self.ask_category(list_category)

    def ask_product(self, list_product):
        """To ask the costumer to choose a product"""
        id_list = []
        print("___________________________________")
        print("Which product would you like to substitute?")
        print("___________________________________")
        # select 10 randoms products
        random_select = choices(list_product, k=10)
        for item in random_select:
            print("Product's number: {}".format(item[0]))
            print("Product's name: {}".format(item[1]))
            print("Nutriscore: {}".format(item[2]))
            # if there is no stores register, print a message
            if item[3] == "":
                print("Sorry, no store has been founded")
            else:
                print("Store (where to find it): {}".format(item[3]))
            print("internet link: {}".format(item[4]))
            print("___________________________________")
            id_list.append(item[0])
        try:
            user_input = int(input("number chosen: "))
            if user_input in id_list:
                return user_input
            return self.ask_product(list_product)
        except ValueError:
            print("sorry can you enter an existing product's number?")
            return self.ask_product(list_product)

    def substitute_chosen(self, sub_prod):
        """Method of view after finding a product
        to show all the informations belonging to it"""
        result = sub_prod[0]
        print("___________________________________")
        print("we found a substitute! ")
        print("We propose you : {}".format(result[1]))
        print("The nutri-score for this product is: {}".format(result[2]))
        # if there is no stores register, print a message
        if result[3] == "":
            print("Sorry, no store has been founded.")
        else:
            print("You can find it by this store : {}".format(result[3]))
        print("You can also just clic on this link: {}".format(result[4]))
        print("___________________________________")
        return result

    def sub_information(self, data):
        """To show the information about
        all the substitute saved in database"""
        number = 1
        for info in data:
            print("___________________________________")
            print("Substitute N°{}: '{}' ".format(number, info[0]))
            print("the nutriscore is '{}'".format(info[1]))
            # if there is no stores register, print a message
            if info[2] == " ":
                print("Sorry, no information about the store is available.")
            else:
                print("You can find it there: {}".format(info[2]))
            print("For more information, clic on the link: {}".format(info[3]))
            number += 1

    def question(self):
        """Question input to start the program and
        ask what the client wants to search or check"""
        question = input(
            "To search a product and his substitute tape: 'a' "
            "To search your substitute selection tape: 'b', "
            "TO quite the program tape: 'q' "
        )
        return question

    def proposal(self):
        """Question input to ask for saving or not the substitute"""
        proposal = input(
            "Do you want to add this product "
            "to your favorite substitute? (y/n):"
        )
        return proposal

    def already_saved(self):
        """Message: You already saved this product"""
        saved = print("You already saved this product.")
        return saved

    def correctly_saved(self):
        """Message: You substitute has been correctly saved!"""
        correct = print("You substitute has been correctly saved!")
        return correct

    def no_save_wish(self):
        """Message after asking to quite the program"""
        no = print("See you soon! Maybe! I don't know!")
        return no

    def sub_not_find(self):
        """Message: Sorry no healthier product has been find"""
        nope = print("Sorry no healthier product has been find :(")
        return nope

    def bye(self):
        """Good bye message"""
        bye = print("Thank you and see you soon!")
        return bye


class DataBase:
    """Class to enter and manipulate the database"""
    def __init__(self, user, password):
        """Initialize the attribute of the database class"""
        self.mysql = mysql.connector.connect(
            user=user,
            password=password,
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
        table_product = "CREATE TABLE product " \
                        "(id SMALLINT  NOT NULL AUTO_INCREMENT," \
                        "PRIMARY KEY(id)," \
                        "name VARCHAR(200)," \
                        "nutri CHAR(1)," \
                        "stores VARCHAR (200)," \
                        "url VARCHAR(200)," \
                        "id_category SMALLINT NOT NULL," \
                        "CONSTRAINT fk_product_category " \
                        "FOREIGN KEY(id_category) " \
                        "REFERENCES category(id)) " \
                        "ENGINE = INNODB"
        # the substitute Table is simple
        # because it will be 'join' to the product table later.
        # Better not to repeat information
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

    def select_category(self):
        """Method to find the categories names
        inside the category's table"""
        query = "SELECT * FROM category"
        self.mycursor.execute(query)
        data = self.mycursor.fetchall()
        return data

    def insert_cat(self, key, value):
        """Method to insert a new category
        inside the category table in the database"""
        query = "INSERT INTO category (id, name) " \
                "VALUES (%s, %s)"
        var = (key, value)
        self.mycursor.execute(query, var)
        self.mysql.commit()

    def select_products(self, wish_cat):
        """Method to find the information
        about a certain amount of product"""
        query = "SELECT * FROM product WHERE id_category = %s"
        var = (wish_cat,)
        self.mycursor.execute(query, var)
        data = self.mycursor.fetchall()
        return data

    def insert_prod(self, data):
        """Method to insert a new product
        inside the product table in the database"""
        query = "INSERT INTO product (" \
                "name, " \
                "nutri, " \
                "stores, " \
                "url, " \
                "id_category" \
                ") " \
                "VALUES (%s, %s, %s, %s, %s)"
        var = data
        self.mycursor.execute(query, var)
        self.mysql.commit()

    def get_nutriscore(self, id):
        """Method to get the nutriscore from a product"""
        query = "SELECT nutri FROM product " \
                "WHERE id = %s"
        var = (id,)
        self.mycursor.execute(query, var)
        answer = self.mycursor.fetchall()
        return answer[0][0]

    def get_substitute(self, id_category, nutriscore):
        """Method to choose a better nutriscore
        from a product in the category chosen"""
        query = "SELECT * FROM product " \
                "where id_category = %s " \
                "and nutri < %s ORDER by nutri"
        var = (id_category, nutriscore)
        self.mycursor.execute(query, var)
        answer = self.mycursor.fetchall()
        return answer

    def select_substitute(self):
        """Method to join the product and the substitute Table
        to get all the data from a substitute product"""
        query = "SELECT name, nutri, stores, url " \
                "FROM product " \
                "JOIN substitute " \
                "ON product.id = substitute.product_ref"
        self.mycursor.execute(query)
        data = self.mycursor.fetchall()
        return data

    def insert_into_substitute(self, substitute_id):
        """Method to insert into the
        substitute Table a new substitute aliment"""
        query = "INSERT INTO substitute (product_ref) " \
                "VALUES (%s)"
        var = (substitute_id,)
        self.mycursor.execute(query, var)
        self.mysql.commit()

    def find_substitute(self, id):
        """Method to find a substitute with his category id"""
        query = "SELECT * FROM substitute " \
                "WHERE product_ref = %s"
        var = (id,)
        self.mycursor.execute(query, var)
        data = self.mycursor.fetchall()
        return data

    def insert_data(self, amount_wanted):
        """Method to :
        - insert the categories from CONSTANT CATEGORY
        inside the category table
        - take from openfoodfacts API the product
        - insert a certain amount of product inside the product table
        depending of the category they belong"""
        print("Database creation in progres.......")
        self.mycursor.execute("USE purbeurre")
        for key, value in CATEGORY.items():
            self.insert_cat(key, value)
            url = "https://fr.openfoodfacts.org/cgi/search.pl"
            payload = {
                "action": "process",
                "tagtype_0": "categories",
                "tag_contains_0": "contains",
                "tag_0": "{}".format(CATEGORY[key]),
                "sort_by": "unique_scans_n",
                "page_size": "1000",
                "axis_x": "energy",
                "axis_y": ["products_n", "action=display"],
                "json": "1"}
            response = requests.get(url, params=payload)
            package = response.json()
            prod_base = package['products']
            num_prod = 0
            for product in prod_base:
                if num_prod <= amount_wanted:
                    try:
                        data = (
                            product['product_name'],
                            product['nutrition_grades'],
                            product['stores'],
                            product['url'],
                            key
                        )
                        self.insert_prod(data)
                        num_prod += 1
                        print(
                            "the product has been added to the category '{}'"
                            .format(CATEGORY[key])
                        )
                    except KeyError:
                        print("No stores information available")
                    except mysql.connector.Error:
                        print("Error")

    def create_or_connect(self):
        """Method to start the program:
        - if the database exist then we use it
        - if the database doesnt exist
        then car create it to use it"""
        exist = self.db_exist()
        if exist:
            self.use_db()
        else:
            self.create_database()
            self.use_db()
            self.insert_data(1000)


class Controller:
    """class to manage all the program
    importing the database 's class and the view"""
    def __init__(self):
        """Initialization"""
        self.view = View()

    def yaml_loader(self, filepath):
        """Loads the login for the database with a yaml file"""
        with open(filepath, "r") as file:
            login = yaml.load(file, Loader=yaml.FullLoader)
            for name, value in login.items():
                return name, value

    def find_substitute(self):
        """Method to:
        - ask a category
        - ask a product
        - find a substitute for this chosen product"""
        category = self.appli.select_category()
        ask_cat = self.view.ask_category(category)
        product = self.appli.select_products(ask_cat)
        ask_prod = self.view.ask_product(product)
        nutri = self.appli.get_nutriscore(ask_prod)
        substitute = self.appli.get_substitute(ask_cat, nutri)
        return substitute

    def saving_or_not(self, substitute):
        """Method to:
        - ask if the client wants to save this subsitute in data
         - react depending of the answer yes or no"""
        if substitute:
            choice = self.view.substitute_chosen(substitute)
            put_in_sub = self.appli.find_substitute(choice[0])
            go = 1
            while go:
                proposal = self.view.proposal()
                if proposal == "y":
                    if put_in_sub:
                        if substitute[0][0] == put_in_sub[0][1]:
                            self.view.already_saved()
                            go = 0
                    else:
                        self.appli.insert_into_substitute(choice[0])
                        self.view.correctly_saved()
                        go = 0
                if proposal == "n":
                    self.view.no_save_wish()
                    go = 0
        if not substitute:
            self.view.sub_not_find()

    def use_programm(self):
        """Method to start the program
        calling all Methods created"""
        login = self.yaml_loader(" purbeurre/authentification.yaml")
        self.appli = DataBase(login[0], login[1])
        self.appli.create_or_connect()

        run = 1
        while run:
            question = self.view.question()
            if question == "a":
                find = self.find_substitute()
                self.saving_or_not(find)
            if question == "b":
                sub = self.appli.select_substitute()
                self.view.sub_information(sub)
            if question == "q":
                self.view.bye()
                run = 0
