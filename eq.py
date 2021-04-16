import urllib.request
import json

# The usgs earthquake json feed
# We ignore earthquakes smaller then 2.5 magnitude
USGS_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson"
VERSION = 1.0

# Retrieve a json item by name
def getMetaDataItem(name, jsonData):
    if name in jsonData["metadata"]:
        return jsonData["metadata"][name]
    else:
        return ""

# Display the days earthquake data
def displayEarthquakes(data, magnitude):
    # Convert data to json
    jsonData = json.loads(data)

    # Title
    title = getMetaDataItem("title", jsonData)
    print(title)

    # Number of events 
    count = getMetaDataItem("count", jsonData)
    print(str(count) + " earthquake events recorded")

    # Earthquake locations
    for i in jsonData["features"]:
        print(i["properties"]["place"])
    printSection("", True)

    # Filter the events by the magnitude filter from the user
    for i in jsonData["features"]:
        if i["properties"]["mag"] >= magnitude:
            print("%2.1f" % i["properties"]["mag"], i["properties"]["place"])
    printSection("", True)

    # At least 1 person reported the earthqauake
    print("Events that were reported by at least 1 person:")
    for i in jsonData["features"]:
        feltReports = i["properties"]["felt"]
        if feltReports != None:
            if feltReports > 0:
                print("%2.1f" % i["properties"]["mag"], i["properties"]["place"], " reported " + str(feltReports) + " times")


# Get a magnitude from the user
def getMagnitude():
    while True:
        try:
            mag = float(input("Enter a magnitude filter: "))
        except ValueError:
            print("Please enter a valid number")
        else:
            return mag

# print a section with or without a divider
def printSection(data, divider):
    if data:
        print(data)
    if divider == True:
        print("----------------------------------------")

# Main method
def main():
    # Header
    printSection("Earthquakes Today version: " + str(VERSION), True)

    # Get the magnitude filter
    magnitude = getMagnitude()

    # Open the url
    print("Retrieving earthquake data from")
    print(USGS_URL)

    url = urllib.request.urlopen(USGS_URL)
    httpResult = url.getcode()
    if httpResult == 200:
        printSection("Succesfully retrieved earthquake data", True)
        displayEarthquakes(url.read().decode("utf-8"), magnitude)
    else:
        printSection("An error occurred while retrieving data. HttpCode: " + str(httpResult), False)

if __name__ == "__main__":
    main()