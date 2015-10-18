#Does data analysis to find service issues with the bus system

import mysql.connector
import xml.etree.ElementTree
import sys
import time

from passwords import *

class routeDataAnalysis:
    ##################
    #Global Functions#
    ##################

    def findClustering(self):
        #open sql connection
        cnx = mysql.connector.connect(user = hid_user, password = hid_password, database = 'rambler')
        cursor = cnx.cursor()

        gmttime = long(time.time())
        findBorder = gmttime - 120

        query = ("SELECT epochKey, busNumber, nextStop, timeToNextStop FROM rambler "
            "WHERE epochKey BETWEEN %s AND %s")
        start_time = gmttime * 1000
        end_time = findBorder * 1000

        cursor.execute(query, (start_time, end_time))
        for (epochKey, busNumber, nextStop, timeToNextStop) in cursor:
