def setup_database(db):
    SQL = """ CREATE TABLE IF NOT EXISTS apartments (
    ad_number VARCHAR (50) UNIQUE NOT NULL,
    created TIMESTAMP NOT NULL,
    price INT NOT NULL,
    url VARCHAR (2048) UNIQUE NOT NULL,
    title VARCHAR (300) NOT NULL
    );
    """
    if db:
        cursor = db.cursor()
        cursor.execute(SQL)
        db.commit()
        print("Table has been created!")
        # db.close()


# ALTER TABLE apartments
# ADD COLUMN title VARCHAR (300) NOT NULL;


# 'SELECT title, price FROM apartments WHERE title=Zakup bez pozwolenia MSWiA 3 pok Niedźwiednik, price={price};'
