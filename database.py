import mysql.connector


class DataBase:
    """Class to enter the database"""
    def __init__(self, user, password, db_name):
        """Initialize the attribute of the product class"""
        self.user = user
        self.password = password
        self.db_name = db_name
        self.mysql = mysql.connector.connect(
            user=self.user,
            password=self.password,
            host='localhost',
            database=self.db_name)
        self.mycursor = self.mysql.cursor()

    def create_database(self):
        """Method to create a database with 2 tables: category and product"""
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
                        "nutri CHAR(1)," \
                        "stores VARCHAR (50)," \
                        "url VARCHAR(50)," \
                        "id_category SMALLINT NOT NULL," \
                        "CONSTRAINT fk_product_category " \
                        "FOREIGN KEY(product_id) REFERENCES category(id)) " \
                        "ENGINE = INNODB"
        table_favorite = "CREATE TABLE favorite " \
                         "(product_id SMALLINT NOT NULL AUTO_INCREMENT PRIMARY KEY," \
                         "CONSTRAINT fk_products_code FOREIGN KEY(product_id) " \
                         "REFERENCES product(id)) " \
                         "ENGINE = INNODB"

        self.mycursor.execute(opening)
        self.mycursor.execute(using)
        self.mycursor.execute(table_category)
        self.mycursor.execute(table_product)
        self.mycursor.execute(table_favorite)

    def db_created(self):
        info = []
        self.mycursor.execute("SHOW DATABASES LIKE 'purbeurre'")
        for data in self.mycursor:
            info.append(data)
        return info
