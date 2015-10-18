#Pulls data from the NextBus API and puts it into the MySQL table

import mysql.connector
import xml.etree.ElementTree

from passwords import *

class routeSQLpull(object):
    #Blue Route Pull
    #Red
    #Trolley
    #Green

    #Rambler Pull
    def ramblerRoute(self):
        cnx = connection.MySQLConnection(user = hid_user, password = hid_password, host = hid_host, database = 'rambler')
        cursor = cnx.cursor()

        stops = {}
        buses = {}

        buses = activeBuses()
        stops = stops(night)

        for bus in buses:
            epochKey = getEpochKey(bus, night)
            nextStop = findNextStop(stops)
            timeToNextStop(nextStop, bus, night)

            add_data = ("INSERT INTO rambler "
                "(epochKey, bus, nextStop, timeToNextStop)")
            data_bus = (epochKey, bus, nextStop, timeToNextStop)

            cursor.execute(add_data, data_bus)
            cnx.commit()
        cnx.close()

    ##################
    #Global Functions#
    ##################

    # Given a route and a stop abbreviation, returns a list of predictions
    # (in minutes) for the next bus arrivals on the route at the stop.
    def getBusTimes(route, stop):
        from urllib import urlopen as open
        from xml.dom.minidom import parse

        url = "https://gtbuses.herokuapp.com/multiPredictions?stops=" + route + "|" + stop
        predictions = parse(open(url)).getElementsByTagName("prediction")
        return [int(p.getAttribute("seconds")) for p in predictions]

    def findNextStop(stops):
    nextStop
    timeToNextStop = sys.maxint
    for stop in stops:
        times = {}
        times = getBusTimes(night, stop)
        if times[0] < timeToNextStop:
            timeToNextStop = times[0]
            nextStop = stop
    return nextStop

    def activeBuses(route):
        from urllib import urlopen as open
        from xml.dom.minidom import parse

        url = "https://gtbuses.herokuapp.com/locations/" + route
        predictions = parse(open(url)).getElementsByTagName("vehicle")
        return [int(p.getAttribute("id")) for p in predictions]

    def getEpochKey(bus, route):
        from urllib import urlopen as open
        from xml.dom.minidom import parse

        url = "https://gtbuses.herokuapp.com/locations/" + route
        predictions = parse(open(url)).getElementsByTagName("prediction")

        for p in predictions:
            if p.getAttribute("vehicle") == bus:
                return int(parse(open(url)).getElementsByTagName("lastTime").getAttribute("time"))

    def timeToNextStop(nextStop, bus, route):
        from urllib import urlopen as open
        from xml.dom.minidom import parse

        url = "https://gtbuses.herokuapp.com/multiPredictions?stops=" + route + "|" + stop
        predictions = parse(open(url)).getElementsByTagName("prediction")

        for p in predictions:
            if p.getAttribute("vehicle") == bus:
                return int(p.getAttribute("seconds"))

    def stops(route):
    from urllib import urlopen as open
    from xml.dom.minidom import parse

    url = "https://gtbuses.herokuapp.com/routeConfig"
    for r in parse(open(url)).getElementsByTagName("route"):
        if r.getAttribute("tag") ==  route:
            stops = r.getElementsByTagName("stop")
            result = {}

            for stop in stops:
                tag = str(stop.getAttribute("tag"))
                title = str(stop.getAttribute("title"))

                if tag not in result:
                    result[tag] = title

            return result
