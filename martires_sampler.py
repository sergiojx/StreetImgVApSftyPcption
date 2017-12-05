import requests
import urllib, os
import json
import math
import datetime
import time
import re


# Determine if a point is inside a given polygon or not
# Polygon is a list of (x,y) pairs. This function
# returns True or False.  The algorithm is called
# the "Ray Casting Method".

def point_in_poly(x,y,poly):

    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside


# un delta de [0.000180] equivale aprox. a 20m
DELTA = 0.000180
DELTA2 = 0.000360

# zone search template javaScript absolute file system path
# This holds search coordinates

cityZone = 'martires'


imgsJsPath = '/vagrant/ggStreetView/map/localidades/%s/imgs/set_%s.js' % (cityZone, cityZone)
imgsJsDirPath = '/vagrant/ggStreetView/map/localidades/%s/imgs' % cityZone



# Zone polygone
polygon = [
              (-74.072829,4.615417),
              (-74.072962,4.615584),
              (-74.077538,4.622051),
              (-74.078828,4.623891),
              (-74.083199,4.624698),
              (-74.09912,4.60502),
              (-74.099822,4.604288),
              (-74.100368,4.603666),
              (-74.101487,4.602576),
              (-74.102113,4.602005),
              (-74.104091,4.600452),
              (-74.105207,4.599625),
              (-74.107073,4.598244),
              (-74.104456,4.596199),
              (-74.104028,4.595841),
              (-74.103706,4.595455),
              (-74.103669,4.595304),
              (-74.103615,4.595088),
              (-74.103204,4.594661),
              (-74.103117,4.59472),
              (-74.102944,4.594771),
              (-74.102703,4.59479),
              (-74.102498,4.594793),
              (-74.102055,4.594801),
              (-74.099085,4.594919),
              (-74.090716,4.592532),
              (-74.089005,4.59182),
              (-74.088935,4.591918),
              (-74.08532,4.596238),
              (-74.084917,4.596795),
              (-74.08488,4.596845),
              (-74.084099,4.597787),
              (-74.083641,4.598371),
              (-74.083194,4.598962),
              (-74.082756,4.599561),
              (-74.082329,4.600168),
              (-74.081913,4.600782),
              (-74.081508,4.601403),
              (-74.081107,4.60204),
              (-74.077576,4.606896),
              (-74.077216,4.607359),
              (-74.07704,4.607596),
              (-74.07687,4.607836),
              (-74.076703,4.608079),
              (-74.07654,4.608326),
              (-74.076382,4.608574),
              (-74.076228,4.608826),
              (-74.076079,4.60908),
              (-74.075934,4.609337),
              (-74.075793,4.609597),
              (-74.075657,4.609859),
              (-74.075526,4.610123),
              (-74.075405,4.610376),
              (-74.075376,4.61043),
              (-74.075346,4.610483),
              (-74.075315,4.610537),
              (-74.075285,4.61059),
              (-74.075224,4.610697),
              (-74.075194,4.610751),
              (-74.075164,4.610805),
              (-74.075134,4.610858),
              (-74.075104,4.610912),
              (-74.075074,4.610966),
              (-74.075044,4.61102),
              (-74.075014,4.611073),
              (-74.074984,4.611127),
              (-74.074955,4.611181),
              (-74.074925,4.611235),
              (-74.074895,4.611289),
              (-74.074866,4.611343),
              (-74.074836,4.611397),
              (-74.074807,4.611451),
              (-74.074777,4.611505),
              (-74.074748,4.611559),
              (-74.074719,4.611613),
              (-74.074689,4.611668),
              (-74.07466,4.611722),
              (-74.074631,4.611776),
              (-74.074602,4.61183),
              (-74.074573,4.611885),
              (-74.074544,4.611939),
              (-74.074515,4.611993),
              (-74.074486,4.612048),
              (-74.074457,4.612102),
              (-74.074428,4.612156),
              (-74.0744,4.612211),
              (-74.074371,4.612265),
              (-74.074342,4.61232),
              (-74.074314,4.612374),
              (-74.074285,4.612429),
              (-74.074257,4.612484),
              (-74.074229,4.612538),
              (-74.0742,4.612593),
              (-74.074172,4.612648),
              (-74.074144,4.612702),
              (-74.074116,4.612757),
              (-74.074087,4.612812),
              (-74.074059,4.612867),
              (-74.074031,4.612921),
              (-74.074003,4.612976),
              (-74.073976,4.613031),
              (-74.073948,4.613086),
              (-74.07392,4.613141),
              (-74.073892,4.613196),
              (-74.073864,4.613251),
              (-74.073837,4.613306),
              (-74.073809,4.613361),
              (-74.073782,4.613416),
              (-74.073754,4.613471),
              (-74.073727,4.613526),
              (-74.0737,4.613582),
              (-74.073672,4.613637),
              (-74.073618,4.613747),
              (-74.073564,4.613858),
              (-74.07351,4.613968),
              (-74.073483,4.614024),
              (-74.073456,4.614079),
              (-74.073429,4.614135),
              (-74.073403,4.61419),
              (-74.073349,4.614301),
              (-74.073323,4.614357),
              (-74.073296,4.614412),
              (-74.07327,4.614468),
              (-74.073217,4.614579),
              (-74.073191,4.614635),
              (-74.073165,4.614691),
              (-74.073139,4.614746),
              (-74.073112,4.614802),
              (-74.072829,4.615417),
        ]
#                   latitud     longitud                 
initialCordenate = (4.628794, -74.106443)
finalCordenate  =  (4.590111, -74.073715)
imageLatitud = initialCordenate[0]
imageLongitud = initialCordenate[1]
# crate associate image directory and image collection javaScript file
outFile = None
print("new directory: %s" %  imgsJsDirPath)
print("new js file: %s" %  imgsJsPath)
if not os.path.exists(imgsJsDirPath):
	os.makedirs(imgsJsDirPath)
	outFile = open(imgsJsPath, "w+")
	outFile.write("var set_%s =\n [" % (cityZone))
	outFile.close()

outF = open(imgsJsPath, "a")	
flag4comma = False


heading_lists = [0,45,90,135,180,-45,-90,-135]
headingIndex = 0
while imageLatitud >= finalCordenate[0]:
       while imageLongitud <= finalCordenate[1]:
              location = "%f,%f" % (imageLatitud, imageLongitud)
              heading = heading_lists[headingIndex ]
              urlmeta = "https://maps.googleapis.com/maps/api/streetview/metadata?size=600x300&location=%s&fov=100&heading=%i&pitch=0&key={CopyYourKeyHere}" % (location, heading)
              url = "https://maps.googleapis.com/maps/api/streetview?size=600x300&location=%s&fov=100&heading=%i&pitch=0&key={CopyYourKeyHere}" % (location, heading)
              print('location')
              print(location)
              try:
                     r = requests.get(urlmeta)
                     data = json.loads(r.text)
                     print('meta_data')
                     print(data)
                     if r.status_code == 200 and data["status"] == 'OK' and ('oogle' in data["copyright"]):
                            try:
                                   point_x = data['location']['lng']
                                   point_y = data['location']['lat']
                                   if point_in_poly(point_x,point_y,polygon) == True:
                                          dateTime = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
                                          imgName = "%s_%s_%i.jpg" %(data['location']['lat'],data['location']['lng'],heading)
                                          location = "%s,%s" % (data['location']['lat'],data['location']['lng'])
                                          url = "https://maps.googleapis.com/maps/api/streetview?size=600x300&location=%s&fov=100&heading=%i&pitch=0&key={CopyYourKeyHere}" % (location, heading)
                                          print(url)
                                          try:
                                                 urllib.urlretrieve(url, os.path.join(imgsJsDirPath,imgName))
                                                 if flag4comma:
                                                        outF.write(",\n")
                                                 outF.write("{\"name\":\"%s\", \"lat\":%s, \"log\":%s, \"sampletime\":\"%s\", \"heading\":%i}" %(imgName,data['location']['lat'],data['location']['lng'],data['date'],heading))
                                                 flag4comma = True
                                                 print('point is into polygon =)') 
                                                 time.sleep(3)
                                          except(HTTPError, ConnectionError, Timeout, RateLimitExceeded, timeout) as e:
                                                 print("urllib.urlretrieve fail =(: %s" % str(e))
                                                 print("longitud %f latitud %f heading %f" %(imageLongitud, imageLatitud, headingIndex))
                                   else:
                                          print('point is NOT into polygon =(')
                            except(HTTPError, ConnectionError, Timeout, RateLimitExceeded, timeout) as e:
                                   print("image access fail =(: %s" % str(e))
                                   print("longitud %f latitud %f heading %f" %(imageLongitud, imageLatitud, headingIndex))
                     imageLongitud = imageLongitud + DELTA2
                     headingIndex = (headingIndex + 1)%8
              except(HTTPError, ConnectionError, Timeout, RateLimitExceeded, timeout) as e:
                     print("metadata access fail =(: %s" % str(e))
                     print("longitud %f latitud %f heading %f" %(imageLongitud, imageLatitud, headingIndex))
        
       imageLatitud = imageLatitud - DELTA2
       imageLongitud = initialCordenate[1]


print("longitud %f latitud %f heading %f" %(imageLongitud, imageLatitud, headingIndex))      

outF.write("]\n")
outF.close()
	
	

