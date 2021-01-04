
class Link:
    """class to make the link between the category table and the product one"""
    def __init__(self, pk_link, fk_prod_cat, fk_cat_prod):
        self.pklink = pk_link
        self.fk_prod_cat = fk_prod_cat
        self.fk_cat_prod = fk_cat_prod

    def find_data(self, mycursor):
        """Method to find the categories"""
        query = "SELECT EXISTS (select * from category where pk_link= %s)"
        var = self.pklink
        mycursor.execute(query, var)
        data = mycursor.fetchall()
        return data

    def parsing(self, key_table):
        """Method of parsing the categories"""
        num_key = 0
        for e in key_table:
            if num_key <= 10:
                print("the primary key is: ", e[self.pklink])
                print("the foreign key for the category is: ", e[self.fk_cat_prod])
                print("the foreign key for the product is: ", e[self.fk_prod_cat])
                print(".........................")
                num_key += 1
