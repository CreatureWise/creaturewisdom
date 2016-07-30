from urllib import urlopen, urlretrieve
import json
import pandas as pd
from numpy import random



def get_animal(lon, lat, radius = 1):
    '''Finds an animal in the region and returns its lsid, name, 
    scientific name,  site details and image location'''

    url = urlopen('http://biocache.ala.org.au/ws/occurrences/search?q=kingdom:Animalia&lon=%s&lat=%s&radius=%s&sort=year&dir=desc&pageSize=1000'%(lon, lat,radius)).read()


    tmp = json.loads(url)
    data = pd.DataFrame(tmp["occurrences"])
    
    #Remove any that don't have a vernacular name recorded
    data = data[pd.notnull(data['vernacularName'])]

    num_animals = len(data['vernacularName'].unique()) 

    #Choose one and get the details
    choice = data.sample(n=1)

    lsid = choice["speciesGuid"].iloc[0]
    name = choice["vernacularName"].iloc[0]
    science_name = choice["scientificName"].iloc[0] 
    url = "http://bie.ala.org.au/species/%s"%(lsid)


    #Get image details
    image = urlopen('http://bie.ala.org.au/ws/species/%s'%(lsid)).read()
    image_tmp = json.loads(image)
    image_loc = image_tmp["imageIdentifier"] +".jpg"

    #Save image
    urlretrieve("http://images.ala.org.au/image/proxyImageThumbnailLarge?imageId=%s"%(image_tmp["imageIdentifier"]), image_loc)



    return lsid, name, science_name, url, image_loc,  num_animals


def get_location(name = "Sydney"):

    name = name.strip()
    name = name.replace(" ", "%20")

    print "Name",name
    # First find what google things is the location
    query = "https://maps.googleapis.com/maps/api/place/autocomplete/json?input=%s&key=%s&country=Australia"%(name, google_api_key)

    url = urlopen(query).read()

    # print url
    place = json.loads(url)

    print place["predictions"]

    place_id = place["predictions"][0]["place_id"]
    place_name = place["predictions"][0]["description"]
   

    # place_id =  place_id["predictions"][0]["place_id"]


    #Get the place_id and use that to find the long/lat
    coord_query = "https://maps.googleapis.com/maps/api/place/details/json?placeid=%s&key=%s"%(place_id, google_api_key)

    coord_raw = urlopen(coord_query).read()

    coord_dict = json.loads(coord_raw)

    lon = coord_dict["result"]["geometry"]["location"]["lng"]
    lat = coord_dict["result"]["geometry"]["location"]["lat"]
    

    return lon, lat, place_name



if __name__ == "__main__":
    print get_animal(151.209296, -33.868820)