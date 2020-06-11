import mysql.connector
from mysql.connector import errorcode
from scripts import orar_ocr


def check_table_exists(dbcon, tablename):
    dbcur = dbcon.cursor()
    dbcur.execute(("\n"
                   "        SELECT COUNT(*)\n"
                   "        FROM information_schema.tables\n"
                   "        WHERE table_name = '{0}'\n"
                   "        ").format(tablename.replace('\'', '\'\'')))
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True

    dbcur.close()
    return False


def insert_mysql_hours(cnx,ore):

   try:
        mysql_insert_query = """INSERT INTO Laptop (Id, Name, Price, Purchase_date) 
                                  VALUES (%s, %s, %s, %s) """

        records_to_insert = [(4, 'HP Pavilion Power', 1999, '2019-01-11'),
                             (5, 'MSI WS75 9TL-496', 5799, '2019-02-27'),
                             (6, 'Microsoft Surface', 2330, '2019-07-23')]

        cursor = cnx.cursor()
        cursor.executemany(mysql_insert_query, records_to_insert)
        cnx.commit()
        print(cursor.rowcount, "Record inserted successfully into Laptop table")

   except mysql.connector.Error as error:
        print("Failed to insert record into MySQL table {}".format(error))


def mysql_connection(pages):
    try:
        cnx = mysql.connector.connect(user='root',
                                      password='rootalchemy',
                                      database='alchemydb')
        print(check_table_exists(cnx, 'orare'))

        for page in pages:
            print(page.titlu)
            for o in page.ore:
                print(tuple(o))
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cnx.close()


if __name__ == '__main__':
    mysql_connection(orar_ocr.get_pages())

    values_to_insert = [(1, 2, 'a'), (3, 4, 'b'), (5, 6, 'c')]
    print(type(values_to_insert[0]))