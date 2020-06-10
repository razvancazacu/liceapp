import mysql.connector
from mysql.connector import errorcode


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


if __name__ == '__main__':

    try:
        cnx = mysql.connector.connect(user='root',
                                      password='rootalchemy',
                                      database='alchemydb')

        print(check_table_exists(cnx, 'orare'))

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cnx.close()
