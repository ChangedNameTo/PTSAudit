#Pulls data from the NextBus API and puts it into the MySQL table

import mysql.connector
import xml.etree.ElementTree
import sys

from passwords import *

class RouteSQLpull:
    #Blue Route Pull
    #Red
    #Trolley
    #Green

    ##################
    #Global Functions#
    ##################

    # Given a route and a stop abbreviation, returns a list of predictions
    # (in minutes) for the next bus arrivals on the route at the stop.
    def getBusTimes(self, route, stop):
        from urllib import urlopen as open
        from xml.dom.minidom import parse

        url = "https://gtbuses.herokuapp.com/multiPredictions?stops=" + route + "|" + stop
        predictions = parse(open(url)).getElementsByTagName("prediction")
        return [int(p.getAttribute("seconds")) for p in predictions]

    def findNextStop(self, stops):
        timeToNextStop = sys.maxint
        for stop in stops:
            times = []
            times = self.getBusTimes("night", stop)
            if times[0] < timeToNextStop:
                timeToNextStop = times[0]
                nextStop = stop
        return nextStop

    def activeBuses(self, route):
        from urllib import urlopen as open
        from xml.dom.minidom import parse

        url = "https://gtbuses.herokuapp.com/locations/" + route
        predictions = parse(open(url)).getElementsByTagName("vehicle")
        return [int(p.getAttribute("id")) for p in predictions]

    def getEpochKey(self, bus, route):
        from urllib import urlopen as open
        from xml.dom.minidom import parse

        url = "https://gtbuses.herokuapp.com/locations/" + route
        predictions = parse(open(url)).getElementsByTagName("lastTime")

        if predictions[0] != None:
            return predictions[0].getAttribute("time")

    def timeToNextStop(self, nextStop, bus, route):
        from urllib import urlopen as open
        from xml.dom.minidom import parse

        url = "https://gtbuses.herokuapp.com/multiPredictions?stops=" + route + "|" + nextStop
        predictions = parse(open(url)).getElementsByTagName("prediction")

        for p in predictions:
            if int(p.getAttribute("vehicle")) == int(bus):
                return p.getAttribute("seconds")

    def getStopsFromRoute(self, route):
        from urllib import urlopen as open
        from xml.dom.minidom import parse

        url = "https://gtbuses.herokuapp.com/predictions/" + route
        predictions = parse(open(url)).getElementsByTagName("predictions")

        result = {}

        for p in predictions:
            result[p.getAttribute("stopTag")] = p.getAttribute("stopTitle")
        return result

    #Rambler Pull
    def ramblerRoute(self):
        cnx = mysql.connector.connect(user = hid_user, password = hid_password, database = 'rambler')
        cursor = cnx.cursor()

        stopsArray = {}
        timeToNextStop = 0

        stopsArray = self.getStopsFromRoute("night")
        buses = self.activeBuses("night")

        for bus in buses:
            epochKey = self.getEpochKey(bus, "night")
            nextStop = self.findNextStop(stopsArray)
            timeToNextStop = self.timeToNextStop(nextStop, bus, "night")
            busNumber = bus

            add_data = ("INSERT INTO rambler "
                "(epochKey, busNumber, nextStop, timeToNextStop)"
                "VALUES (%s, %s, %s, %s)")
            data_bus = (epochKey, busNumber, nextStop, timeToNextStop)

            cursor.execute(add_data, data_bus)
            cnx.commit()
        cnx.close()

    #Main
routeSQLpull = RouteSQLpull()
routeSQLpull.ramblerRoute()
