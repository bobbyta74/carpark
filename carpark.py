import sqlite3, time
connection = sqlite3.connect("carpark.db")
cursor = connection.cursor()

#Create table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS cars(
        reg TEXT,
        entry REAL
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
        entry = time.time()
        #Add plate and time entered to database
        cursor.execute("""
            INSERT INTO cars(reg, entry)
            VALUES (?, ?)
        """, [ reg, entry ])
        connection.commit()
        secondstoday = entry % (3600*24)
        hours = int(secondstoday // 3600)
        minutes = int((secondstoday % 3600) // 60)
        seconds = int(secondstoday % minutes)
        print(f"Welcome. Time of entry: {hours}:{minutes}:{seconds}")
    else:
        #Output time stayed in seconds
        timedelta = time.time() - result[0]
        print(f"You stayed {timedelta} seconds. Pay up.")
        print("Goodbye.")
        cursor.execute("""
            DELETE FROM cars WHERE reg = ?
        """, [ reg ])

connection.close()