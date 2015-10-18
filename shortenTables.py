#MySQL tables will become too bloated with data to parse effectively
#this trims the tables

import mysql.connector
import sys
import time
from passwords import *

class ShortenTables:
    ##################
    #Global Functions#
    ##################
    def ramblerTableTrim(self):
        #open sql connection
        cnx = mysql.connector.connect(user = hid_user, password = hid_password, database = 'rambler')
        cursor = cnx.cursor()

        gmttime = long(time.time())
        deletionBorder = gmttime - 3600

        print deletionBorder * 1000

        delete_data = ("DELETE FROM rambler "
            "WHERE epochKey < %s")
        cursor.execute(delete_data, (deletionBorder,))

        cnx.commit()
        cnx.close()

shortenTables = ShortenTables()
shortenTables.ramblerTableTrim()
