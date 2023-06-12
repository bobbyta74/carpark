import sqlite3, time
connection = sqlite3.connect("carpark.db")
cursor = connection.cursor()

#Create table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS cars(
        reg TEXT,
        entry INTEGER
    )
""")
connection.commit()

reg = ""
while reg != "exit":
    reg = input("Enter registration (or \"exit\" to exit): ")
    #Check whether plate already in database (value of reg variable injected into question mark)
    result = cursor.execute("""
        SELECT entry FROM cars
        WHERE reg = ?
    """, [ reg ]).fetchone()

    if result == None:
        #Add plate and time entered to database
        cursor.execute("""
            INSERT INTO cars(reg, entry)
            VALUES (?, ?)
        """, [ reg, time.time() ])
    else:
        #Output time stayed in seconds
        timedelta = time.time() - result[0]
        print("Length of stay:", timedelta)