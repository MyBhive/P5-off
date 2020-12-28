import mysql.connector
import requests

# API
response = requests.get("https://be-fr.openfoodfacts.org/cgi/search.pl?"
                        "search_simple=1&action=process&tagtype_0=categories&"
                        "tag_contains_0=contains&tag_0=pizza&"
                        "sort_by=ciqual_food_name_tags&page_size=200&json=1")

# lecture des données
package = response.json()
prod_base = package['products']

prod_name = 'product_name'
name_fr1 = 'ecoscore_data'
name_fr2 = 'agribalyse'
name_fr3 = 'agribalyse_food_name_fr'
nutri = 'nutrition_grades'
url = 'url'


# recherche de données
def find_data():
    num_product = 0
    for e in prod_base:
        if num_product <= 20:
            print(e[prod_name])
            print(e[nutri])
            print(e[url])
            num_product += 1


cnx = mysql.connector.connect(user='root', password='Gab03nas18',
                              host='localhost', database='people')

mycursor = cnx.cursor()


def create_database():
    mycursor.execute("CREATE TABLE Contact "
                     "(prenom VARCHAR(30) NOT NULL,"
                     "nom VARCHAR(30) NOT NULL,"
                     "telephone CHAR(12),"
                     "id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,"
                     "PRIMARY KEY (id)) "
                     "ENGINE = INNODB;")


def insert_into_table():
    mycursor.execute("INSERT INTO Contact "
                     "(prenom, nom, telephone) "
                     "VALUES ('jean', 'lebul', '0609562005'),"
                     "('marc', 'papin', '0627281130'),"
                     "('robert', 'matin', '06083234104'),"
                     "('jean', 'bulbe', '0636656565')")


cnx.commit()

for i in mycursor:
    print(i)


# demander à voir les infos de la table
def extract_info():
    mycursor.execute("describe contact")


# suivre ce modele
def extract_prenom():
    query = "select * from contact where prenom= %s"
    var = ("robert",)
    mycursor.execute(query, var)
    data = mycursor.fetchone()
    print(data)


# chercher un contact avec son nom et prenom
def extract_nom_prenom(prenom, nom):
    query = "select * from contact where prenom= %s and nom=%s"
    var = (prenom, nom)
    mycursor.execute(query, var)
    data = mycursor.fetchall()
    print(data)


def alpha_order():
    query = "select * from contact order by nom asc"
    mycursor.execute(query)
    data = mycursor.fetchall()
    print(data)


def favoris_insert(prenom, nom, telephone):
    query = "INSERT INTO contact (prenom, nom, telephone) VALUES (%s, %s, %s)"
    var = (prenom, nom, telephone)
    mycursor.execute(query, var)
    cnx.commit()


def delete_info(prenom, id):
    query = "DELETE FROM contact WHERE prenom = %s and id = %s"
    var = (prenom, id)
    mycursor.execute(query, var)
    cnx.commit()


# appel de la méthode pour la tester
alpha_order()
