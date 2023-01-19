import sqlite3
from sqlite3 import Error

class queries:
    def main(self):
        self.FetchMainAllergiesCalories("Guacamole and chips")
        self.FetchMenu("Guacamole and chips")

    def DatabaseConnection(self):
        conn = None
        try:
            conn = sqlite3.connect("Menu.db")
        except Error as e:
            print(e)

        return conn

    def FetchMainAllergiesCalories(self, Input):
        conn = self.DatabaseConnection()
        a = (conn.execute("SELECT Calories FROM MENU,Alergies WHERE MENU.Name = '"+ Input +"' LIMIT 1"))
        b = (conn.execute("SELECT Name, "
                        + "(CASE WHEN gluten = TRUE THEN 'gluten ' ELSE '' END) || "
                        + "(CASE WHEN peanuts = TRUE THEN 'peanuts ' ELSE '' END) || "
                        + "(CASE WHEN treenuts = TRUE THEN 'treenuts ' ELSE '' END) || "
                        + "(CASE WHEN celery = TRUE THEN 'celery ' ELSE '' END) || "
                        + "(CASE WHEN mustard = TRUE THEN 'mustard ' ELSE '' END) || "
                        + "(CASE WHEN eggs = TRUE THEN 'eggs ' ELSE '' END) || "
                        + "(CASE WHEN milk = TRUE THEN 'milk ' ELSE '' END) || "
                        + "(CASE WHEN sesame = TRUE THEN 'sesame ' ELSE '' END) || "
                        + "(CASE WHEN fish = TRUE THEN 'fish ' ELSE '' END) || "
                        + "(CASE WHEN crustaceans = TRUE THEN 'crustaceans ' ELSE '' END) || "
                        + "(CASE WHEN molluscs = TRUE THEN 'molluscs ' ELSE '' END) || "
                        + "(CASE WHEN sulphites = TRUE THEN 'sulphites ' ELSE '' END) || "
                        + "(CASE WHEN lupin = TRUE THEN 'lupin ' ELSE '' END) " 
                        + "FROM Alergies "
                        + "WHERE Name = '"+ Input +"';"))
        rows = a.fetchall()
        results = b.fetchall()
        for row in rows:
            print(row[0])
        for result in results:
            print(result)
        conn.commit()

    def FetchMenu(self,Input):
        conn = self.DatabaseConnection()
        a = (conn.execute("SELECT Name, price "
                        + "FROM Menu "
                        + "WHERE Name = '"+ Input + "';"))
        results = a.fetchall()
        for result in results:
            print(result)

q = queries()
q.main()