import flask, time, sqlite3

def initialise_db():
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
    connection.close()

initialise_db()
app = flask.Flask(__name__)

@app.route("/")
def front():
    return "hello from flask"

@app.route("/park", methods = ["GET"])
def park():
    connection = sqlite3.connect("carpark.db")
    cursor = connection.cursor()

    reg = ""
    while reg != "exit":
        reg = flask.request.args.get("reg")
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
            return {
                "type" : "entry",
                "time" : entry
            }
        else:
            #Output time stayed in seconds
            timedelta = time.time() - result[0]
            cursor.execute("""
                DELETE FROM cars WHERE reg = ?
            """, [ reg ])
            connection.commit()
            return {
                "type" : "departure",
                "duration" : timedelta
            }

    connection.close()