import mysql.connector
import requests


""" constant data for the purbeurre application"""
CATEGORY = {
    1: "surgeles",
    2: "pizzas",
    3: "chocolats",
    4: "soupes",
    5: "boissons"
}


class Category:
    """Class to handle a category object: to find,
    to parse or to insert in database"""
    def __init__(self, id, name):
        """Initialize the attribute of the category class"""
        self.id = id
        self.name = name


class Product:
    """Class to handle a product object: to find,
    to parse or to insert in database"""

    def __init__(self, name, nutri, store, url, category):
        """Initialize the attribute of the product class"""
        # lecture des donnees
        self.name = name
        self.nutri = nutri
        self.store = store
        self.url = url
        self.id = category


class Substitute:
    """Class to handle a substitute object: to find,
    to parse or to insert in database"""

    def __init__(self, substitute_id, product_ref):
        """Initialize the attribute of the product class"""
        # lecture des donnees
        self.substitute_id = substitute_id
        self.product_ref = product_ref


class View:
    def __init__(self):
        pass

    def ask_category(self, list_category):
        print("___________________________________")
        print("Select the category of your choice: ")
        print("___________________________________")
        for item in list_category:
            print("Category's number: {}".format(item[0]))
            print("Category's name: {}".format(item[1]))

        try:
            user_input = int(input("number chosen: "))
            if 0 <= user_input >= 5:
                return self.ask_category(list_category)
            return user_input
        except:
            return self.ask_category(list_category)

    def ask_product(self, list_product):
        print("___________________________________")
        print("Which product would you like to substitute?")
        print("___________________________________")
        for item in list_product:
            print("Product's number: {}".format(item[0]))
            print("Product's name: {}".format(item[1]))
            print("Nutriscore: {}".format(item[2]))
            print("Store (where to find it): {}".format(item[3]))
            print("internet link: {}".format(item[4]))
        try:
            user_input = int(input("number chosen: "))
            if 0 <= user_input >= 10:
                return self.ask_product(list_product)
            return user_input
        except:
            return self.ask_product(list_product)

    def substitute_chosen(self, sub_prod):
        """Method to find the information
        about a certain amount of product"""
        result = sub_prod[0]
        print("___________________________________")
        print("we found a substitute! ")
        print("We propose you a '{}".format(result[0]))
        print("The nutri-score for this product is: {}".format(result[1]))
        print("You can find it by this distributor : {}".format(result[2]))
        print("You can also just clic on this link: {}".format(result[3]))
        print("___________________________________")
        return result

    def show_substitute(self, data):
        for info in data:
            print("You have chosen '{}' has substitute".format(info[0]))
            print("the nutriscore is '{}'".format(info[1]))
            print("You can find it on this store: {}".format(info[2]))
            print("For more information, clic on the link: {}".format(info[3]))
            return info


class DataBase:
    """Class to enter and manipulate the database"""
    def __init__(self, user, password):
        """Initialize the attribute of the product class"""
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

    def select_category(self):
        """Method to find the categories"""
        query = "SELECT EXISTS (SELECT * FROM category)"
        self.mycursor.execute(query)
        data = self.mycursor.fetchall()
        return data

    def insert_cat(self, key, value):
        """Method to insert a new category inside the category database"""
        query = "INSERT INTO category (id, name) " \
                "VALUES (%s, %s)"
        var = (key, value)
        self.mycursor.execute(query, var)
        self.mysql.commit()

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

    def get_nutriscore(self, id):
        """Method to get the nutriscore from a product"""
        query = "SELECT EXISTS " \
                "(SELECT nutri FROM product " \
                "WHERE id = %s)"
        var = id
        answer = self.mycursor.execute(query, var)
        return answer

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
        self.mycursor.fetchall()

    def insert_into_substitute(self, substitute_id):
        """Method to insert into the
        substitute Table a new substitute aliment"""
        query = "INSERT INTO substitute (substitute_id) " \
                "VALUES (%s)"
        var = substitute_id
        self.mycursor.execute(query, var)
        self.mysql.commit()

    def find_substitute(self, id):
        """Method to find the categories"""
        query = "SELECT EXISTS " \
                "(SELECT * FROM substitute " \
                "WHERE product_id= %s)"
        var = id
        self.mycursor.execute(query, var)
        data = self.mycursor.fetchall()
        return data

    def insert_data(self, amount_wanted):
        """méthode qui va chercher les categories et
        produits sur l'api pour les enregistrer dans la db"""
        print("Database creation in progres.......")
        self.mycursor.execute("USE purbeurre")
        num_prod = 0
        for key, value in CATEGORY.items():
            self.insert_cat(key, value)
            while num_prod <= amount_wanted:
                url = "https://fr.openfoodfacts.org/category/{}.json".format(CATEGORY[key])
                response = requests.get(url)
                package = response.json()
                prod_base = package['products']
                try:
                    for product in prod_base:
                        data = {
                            'name': product['product_name'],
                            'nutri': product['nutrition_grades'],
                            'stores': product['stores'],
                            'url': product['nutrition_grades'],
                            'id_category': key
                        }
                        self.insert_prod(data)
                        num_prod += 1
                except:
                    self.mysql()


class Controller:
    """ class to manage all the programm
    importing all the others classes"""
    def __init__(self):
        """Initialization"""
        self.appli = DataBase(user="root", password="Gab03nas18")
        self.view = View()

    def use_programm(self):
        exist = self.appli.db_exist()
        if exist:
            self.appli.use_db()
            self.appli.insert_data(10)
        else:
            self.appli.create_database()
            self.appli.use_db()
            self.appli.insert_data(10)

        run = 1
        while run:
            question = input(
                "To search a product and his substitute tape: 'O' "
                "To search your substitute selection tape: 'Y', "
                "TO quite the program tape: 'Q' "
            )
            if question == "O":
                category = self.appli.select_category()
                ask_cat = self.view.ask_category(category)

                product = self.appli.select_products(ask_cat)
                ask_prod = self.view.ask_product(product)

                nutri = self.appli.get_nutriscore(ask_prod)
                #on met les sub du meilleur au moins bon
                substitute = self.appli.get_substitute(ask_cat, nutri)

                if substitute:
                    self.view.substitute_chosen(substitute)
                    # ajouter au sub si pas deja fait
                    put_in_sub = self.appli.find_substitute(substitute[0])
                    if put_in_sub[0][0] == 0:
                        proposal = input("Do you want to add this product to your favorite substitute? (y/n):")
                        if proposal == "y":
                            self.appli.insert_into_substitute(substitute[0])
                        if proposal == "n":
                            print("see you soon maybe i don't know can you repeat the question")
                            run = 0
                        else:
                            print("You already saved this product.")
                else:
                    print("Sorry no healthier product has been find :(")

            if question == "Y":
                self.appli.select_substitute()
                # self.view.show_substitute(data)
                # si ca ne marche pas passer ces 2 methodes en 1


            if question == "Q":
                print("Thank you and see you soon!")
                run = 0

            else:
                print("please enter O, Y or Q")

    def check(self):
        for key, value in CATEGORY.items():
            self.appli.insert_cat(key, value)


bob = DataBase('root','Gab03nas18')
pop = Controller()
bob.use_db()
bob.insert_data(10)

