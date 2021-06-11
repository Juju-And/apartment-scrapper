from psycopg2 import connect, OperationalError

username = "postgres"
passwd = "coderslab"
hostname = "127.0.0.1"  # lub "localhost"
db_name = "apartments"


def create_connection(username, passwd, hostname, db_name):
    try:
        cnx = connect(user=username, password=passwd, host=hostname, database=db_name)
        print("Connection successful.")
        return cnx
    except OperationalError:
        print("Connection failed.")
        return None


def add_apartment(ad_number, created, price, url):
    SQL = """INSERT INTO apartments(name, description, price) VALUES ('{}', '{}', {}, '{}');""".format(
        ad_number, created, price, url,
    )
    print(SQL)
    return SQL


context = create_connection(username, passwd, hostname, db_name)
prepared_statement = add_apartment(apartment)
