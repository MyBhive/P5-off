import mysql.connector


class Database:
    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.mysql = mysql.connector.connect\
            (user=self.user,
             password=self.password,
             host='localhost')
        self.mycursor = self.mysql.cursor()

    def create_database(self):
        opening = "CREATE DATABASE purbeurre CHARACTER SET 'utf8'"
        using = "USE purbeurre"
        # creating a table category : the id is not auto increment to choose one per category
        # exemple : 1 for pizza, 2 for frozen, 3 for cakes etc
        table_category = "CREATE TABLE category " \
                         "(id SMALLINT NOT NULL PRIMARY KEY," \
                         "name VARCHAR(30)) " \
                         "ENGINE = INNODB"
        # creating a table product to integrate the products and all their data
        # id, name, brand, nutriscore, stores, url and
        # id category and the foreign key to the table category
        table_product = "CREATE TABLE product " \
                        "(id SMALLINT NOT NULL AUTO_INCREMENT PRIMARY KEY," \
                        "name VARCHAR(50)," \
                        "brand VARCHAR (50)," \
                        "nutri CHAR(1)," \
                        "stores VARCHAR (50)," \
                        "url VARCHAR(50)," \
                        "id_category SMALLINT NOT NULL," \
                        "CONSTRAINT fk_products_code " \
                        "FOREIGN KEY(product_id) REFERENCES category(id)) " \
                        "ENGINE = INNODB"
        self.mycursor.execute(opening)
        self.mycursor.execute(using)
        self.mycursor.execute(table_category)
        self.mycursor.execute(table_product)

    def use(self):
        use = "USE purbeurre"
        self.mycursor.execute(use)

    def show_base(self):
        show = "SHOW DATABASES"
        self.mycursor.execute(show)
        for element in self.mycursor:
            return element

# aller chercher le produit sur openfoodfacts et le mettre dans la base de données
# méthode qui travaille avec l'API et requests
    def insert_data(self, id, name):
        pass

# supprimer un élément (si celui est en double ou non nécessaire)
    def delete_data(self):
        pass

    def select_category(self):
        selection = "SELECT * FROM category"
        self.mycursor.execute(selection)
        result = self.mycursor.fetchall()
        return result

    def select_product(self):
        selection = "SELECT * FROM product"
        self.mycursor.execute(selection)
        result = self.mycursor.fetchall()
        return result

    def choose_category(self):
        input("quelle catégorie d'aliment désirez-vous?")
        pass

    def choose_product(self):
        input("quel aliment désirez-vous?")
        # sans doute créer un liste des produits et sélectionner un produit grâce à son id ou indice
        pass
