from psycopg2 import connect, OperationalError

from main import generate_import_dict

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


def add_apartment(apartments: dict):
    SQL = "INSERT INTO apartments(ad_number, created, price, url) VALUES "
    counter = 0
    for key, value in apartments.items():
        SQL += """('{}', '{}', {}, '{}')""".format(
            value["ad_number"], value["created"], value["price"], value["url"],
        )
        if counter < len(apartments.items()) - 1:
            SQL += ","
        counter += 1
    SQL += ";"
    return SQL


context = create_connection(username, passwd, hostname, db_name)

apartments = generate_import_dict()
prepared_statement = add_apartment(apartments)

if context:
    cursor = context.cursor()
    cursor.execute(prepared_statement)
    context.commit()
    print('Apartments added to the database!')
    context.close()
