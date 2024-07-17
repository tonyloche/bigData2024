import mysql.connector

cnx = mysql.connector.connect(user='root', password='Tonyissexy1',host='127.0.0.1',database='myfirstdb')

cursor = cnx.cursor()

#inserting data in person table 
add_player = "INSERT INTO persons (PersonID, LastName, FirstName, City, Sport) VALUES (8,'james','lebron','baseball','cleveland')"
cursor.execute(add_player)

cursor.execute("SELECT * FROM persons;")
for row in cursor:
    print(row)

cnx.commit()

cursor.close()
cnx.close()