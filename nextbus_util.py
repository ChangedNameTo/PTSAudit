# Given any number of stop abbreviations, returns a list of dictionaries,
# each of which corresponds to a single stop for a single route going in a 
# single direction. Each dictionary has the following key-pair values:
#
# "route"     : the abbreviated route name (e.g. "trolley")
# "routeName" : the actual name of the route (e.g. "Tech Trolley")
# "direction" : the last stop of the route moving in this direction 
#               (e.g. "North Ave Apartments" for Red Route)
# "stop"      : the stop abbreviation passed as an argument to this function
#               which corresponds to this route
# "stopName:  : the actual name of the stop associated with this route.
#
# The purpose of this function is to gather the information necessary to call
# getBusTimes (the stop abbreviation and the route abbreviation), along with 
# pertinent information for displaying the Bus times (the route name, stop name,
# and direction) and store all this information in one dictionary per route
# being considered.
def getRouteInformation(*stops):
    from urllib import urlopen as open
    from xml.dom.minidom import parse
    url = "https://gtbuses.herokuapp.com/routeConfig"
    page = parse(open(url))
    
    stopNames = {}
    for stopTag in page.getElementsByTagName("stop"):
        stop = stopTag.getAttribute("tag")
        
        if stop in stops and stopTag.parentNode.tagName == "route":
            stopNames[stop] = stopTag.getAttribute("title")
    
    routes = []
    for routeTag in page.getElementsByTagName("route"):
        route = routeTag.getAttribute("tag")
        for directionTag in routeTag.getElementsByTagName("direction"):
            direction = directionTag.getAttribute("title")
            for stopTag in directionTag.getElementsByTagName("stop"):
                stop = stopTag.getAttribute("tag")
                
                if stop in stops:
                    info = {"route": route, "direction": direction,
                            "routeName": routeTag.getAttribute("title"),
                            "stop": stop, "stopName": stopNames[stop]} 
                    routes.append(info)
                    
    return routes

# Returns a list of the names of all available routes.
def getAllRoutes():
    from urllib import urlopen as open
    from xml.dom.minidom import parse
    
    url = "https://gtbuses.herokuapp.com/routeConfig"
    routes = parse(open(url)).getElementsByTagName("route")
    return [str(route.getAttribute("tag")) for route in routes]

            
# Returns a list of all stop abbreviations for a given route (red, blue, green,
# trolley, emory, etc.).
def getStops(route):
    from urllib import urlopen as open
    from xml.dom.minidom import parse
    route = route.lower()
    
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
            
    raise ValueError("Route \"" + route + "\" does not exist.")

    
# Generates a file with the given filename in which all abbreviations and
# stop names are listed for each route.    
def makeStopFile(filename):
    f = file(filename, "w")
    for route in getAllRoutes():
        f.write(route + ":\n")
        for abbreviation, title in getStops(route).items():
            spaces = " " * (26 - (4 + len(abbreviation)))
            f.write("\t" + abbreviation + ":" + spaces + title + "\n")
        f.write("\n")
    f.close()

    
# Given any number of stop abbreviations, returns a list of tuples of the form
# (route, stop), where stop is a stop whose abbreviation occurs in the given
# abbreviations and route is a route which passes through that stop.
def getRoutes(*stopNames):
    from urllib import urlopen as open
    from xml.dom.minidom import parse
    
    url = "https://gtbuses.herokuapp.com/routeConfig"
    stops = parse(open(url)).getElementsByTagName("stop")
    return [(s.parentNode.getAttribute("tag"), s.getAttribute("tag"))
            for s in stops if s.getAttribute("tag") in stopNames
            and s.parentNode.tagName == "route"]

    
# Given a route and a stop abbreviation, returns a list of predictions
# (in minutes) for the next bus arrivals on the route at the stop.
def getBusTimes(route, stop):
    from urllib import urlopen as open
    from xml.dom.minidom import parse
    
    url = "https://gtbuses.herokuapp.com/multiPredictions?stops=" + route + "|" + stop
    predictions = parse(open(url)).getElementsByTagName("prediction")
    return [int(p.getAttribute("minutes")) for p in predictions]

