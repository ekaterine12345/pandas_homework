import psycopg2

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    dbname="experiment",
    user="postgres",
    password="Super1",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()

# Create experiments table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS experiments (
        experiment_id SERIAL PRIMARY KEY,
        experiment_name VARCHAR(1024),
        property_name VARCHAR(2056),
        property_value VARCHAR(2056)
    );
''')

# Create plates table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS plates (
        plate_id SERIAL PRIMARY KEY,
        plate_name VARCHAR(1024),
        experiment_id INTEGER REFERENCES experiments(experiment_id),
        property_name VARCHAR(2056),
        property_value VARCHAR(2056)
    );
''')

# Create wells table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS wells (
        well_id SERIAL PRIMARY KEY,
        well_row VARCHAR(2),
        well_column VARCHAR(2),
        plate_id INTEGER REFERENCES plates(plate_id),
        property_name VARCHAR(2056),
        property_value VARCHAR(2056)
    );
''')

conn.commit()
cursor.close()
conn.close()
