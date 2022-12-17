import pyodbc 

def connectDB():
    try:
        conn = pyodbc.connect('Driver={SQL SERVER};'
                      'Server=LYTRAN\SERVER;'
                      'Database=HTTM;'
                      'Trusted_Connection=yes;')
        print("Connected")
        return conn
    except:
        print("Connect Fail")

def getSounds():
    conn = connectDB()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sound')

    return cursor

def getSoundById(id):
    conn = connectDB()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sound WHERE id=?',[id])

    return list(cursor.fetchall())[0]

def getSoundByName(name):
    conn = connectDB()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sound WHERE name=?',[name])

    return list(cursor.fetchall())[0][0]

def getDrivers():
    conn = connectDB()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM driver')

    return list(cursor.fetchall())


def getLogin(id, password):
    conn = connectDB()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM driver WHERE id=? and password=?',[id, password])

    return cursor

def getDriverById(idDriver):
    conn = connectDB()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM driver WHERE id=?',[idDriver])

    return list(cursor.fetchall())[0]

def updateSound(idDriver, idSound, time):
    conn = connectDB()
    try:
        cursor = conn.cursor()
        cursor.execute('''UPDATE driver SET id_song = ?, timeAlarm = ? WHERE id = ?''',[idSound, time, idDriver])
        conn.commit()
        return True
    except Exception as e:
        print("errors", e)
        return False


def saveDriver(driver):
    conn = connectDB()
    id = driver.get("id")
    name = driver.get("name")
    gender = driver.get("gender")
    age = driver.get("age")
    license = driver.get("license")
    password = driver.get("password")
    try:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO driver (id, name, gender, age, license, id_song, timeAlarm, password) VALUES(?,?,?,?,?,?,?,?)''',id, name, gender, age, license,1,10,password)
        conn.commit()
        return True
    except Exception as e:
        print("errors", e)
        return False

def updateDriver(driver):
    print("update driver")
    print("driver", driver)
    conn = connectDB()
    id = driver.get("id")
    name = driver.get("name")
    gender = driver.get("gender")
    age = int(driver.get("age"))
    license = driver.get("license")
    password = driver.get("password")
    try:
        cursor = conn.cursor()
        cursor.execute('''UPDATE driver SET name = ?, gender = ?, age =?, license=?,password=?  WHERE id = ?''',[name, gender, age, license, password, id])
        conn.commit()
        return True
    except Exception as e:
        print("errors", e)
        return False

