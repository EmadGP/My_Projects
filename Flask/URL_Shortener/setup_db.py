import MySQLdb

db = MySQLdb.connect("localhost", "root", "", "url")
cursor = db.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS urls (
    ORG VARCHAR(255) NOT NULL,
    Shortend VARCHAR(255) NOT NULL,
    PRIMARY KEY (Shortend)
)
""")
db.commit()
db.close()
print("Database setup complete.")
