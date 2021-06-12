from psycopg2 import connect, OperationalError


def create_db_context() -> None:
    username = "postgres"
    passwd = "coderslab"
    hostname = "127.0.0.1"  # lub "localhost"
    db_name = "apartments"
    try:
        cnx = connect(user=username, password=passwd, host=hostname, database=db_name)
        print("Connection successful.")
        return cnx
    except OperationalError:
        print("Connection failed.")
        return None


def create_sql_insert_apartment(apartment) -> str:
    SQL = """INSERT INTO apartments(ad_number, created, price, url) VALUES ('{}', '{}', {}, '{}')""".format(
        apartment["ad_number"],
        apartment["created"],
        apartment["price"],
        apartment["url"],
    )

    return SQL


def apartment_exists(db, number) -> bool:
    records = []
    if db:
        cursor = db.cursor()
        cursor.execute("SELECT ad_number FROM apartments;")
        records = cursor.fetchall()

    if list(filter(lambda x: str(number) in x, records)):
        print("Apartment already in db!")
        return True


def add_apartment(db, apartment) -> None:
    if db:
        cursor = db.cursor()
        cursor.execute(create_sql_insert_apartment(apartment))
        db.commit()
        print("Apartments added to the database!")
        # db.close()
