from psycopg2 import connect, OperationalError
from dotenv import dotenv_values

config = dotenv_values(".env")


def create_db_context():
    username = config['USERNAME']
    passwd = config['PASSWD']
    hostname = config['HOSTNAME']
    db_name = config['DB_NAME']
    try:
        cnx = connect(user=username, password=passwd, host=hostname, database=db_name)
        print("Connection successful.")
        return cnx
    except OperationalError:
        print("Connection failed.")
        return None


def create_sql_insert_apartment(apartment) -> str:
    SQL = """INSERT INTO apartments(ad_number, created, price, url, title) VALUES ('{}', '{}', {}, '{}', '{}')""".format(
        apartment["ad_number"],
        apartment["created"],
        apartment["price"],
        apartment["url"],
        apartment["title"],
    )

    return SQL


def apartment_exists(db, ad_number) -> bool:
    if db:
        cursor = db.cursor()

        cursor.execute("select * from apartments where ad_number = %s;", (ad_number,))
        records = cursor.fetchone()

        if records is not None:
            return True


def add_apartment(db, apartment) -> None:
    if db:
        cursor = db.cursor()
        cursor.execute(create_sql_insert_apartment(apartment))
        db.commit()
        print("Apartments added to the database!")
        # db.close()
