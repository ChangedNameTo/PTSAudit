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
