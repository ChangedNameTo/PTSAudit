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
    def tableTrim(self, table):
        currentTime = time.gmtime()
