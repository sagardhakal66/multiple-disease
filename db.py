


import sqlite3

# Create a connection to the database
conn = sqlite3.connect('test.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create a table for diabetes prediction data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Diabetes (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Pregnancies INTEGER,
        Glucose REAL,
        BloodPressure REAL,
        SkinThickness REAL,
        Insulin REAL,
        BMI REAL,
        DiabetesPedigreeFunction REAL,
        Age INTEGER,
        Prediction TEXT
    )
''')

# Create a table for heart disease prediction data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Heart (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Age INTEGER,
        Sex INTEGER,
        ChestPainTypes INTEGER,
        RestingBloodPressure REAL,
        SerumCholestoral REAL,
        FastingBloodSugar INTEGER,
        RestingECG INTEGER,
        MaxHeartRateAchieved REAL,
        ExerciseInducedAngina INTEGER,
        STDepression REAL,
        Slope INTEGER,
        MajorVesselsColored INTEGER,
        Thal INTEGER,
        Prediction TEXT
    )
''')









# Create a table for Parkinson's disease prediction data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS parkinson (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        MDVP_Fo_Hz REAL,
        MDVP_Fhi_Hz REAL,
        MDVP_Flo_Hz REAL,
        MDVP_Jitter_percent REAL,
        MDVP_Jitter_Abs REAL,
        MDVP_RAP REAL,
        MDVP_PPQ REAL,
        Jitter_DDP REAL,
        MDVP_Shimmer REAL,
        MDVP_Shimmer_dB REAL,
        Shimmer_APQ3 REAL,
        Shimmer_APQ5 REAL,
        MDVP_APQ REAL,
        Shimmer_DDA REAL,
        NHR REAL,
        HNR REAL,
        RPDE REAL,
        DFA REAL,
        spread1 REAL,
        spread2 REAL,
        D2 REAL,
        PPE REAL,
        Prediction TEXT
    )
''')



cursor.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        phone INTEGER,
        subject TEXT,
        message TEXT
    )
''')



cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
''')              



# cursor.execute('''
#     DROP TABLE contact
# ''') 


# cursor.execute('''
#     DROP TABLE park
# ''') 


# Commit the changes and close the database connection
conn.commit()
conn.close()











# Example usage:
# save_to_db(1, 'some_prediction')