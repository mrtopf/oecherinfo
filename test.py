

import requests
from urllib.parse import urlparse, parse_qs, urlencode
import pprint

URL1 = "https://services-eu1.arcgis.com/2ypUQspLVcN0KOBE/arcgis/rest/services/CoronavirusFallzahlen_%C3%B6ffentlich/FeatureServer/1/query?f=json&where=(Kommune%3D%27Aachen%27%20AND%20Meldedatum%3Etimestamp%20%272020-03-16%2022%3A59%3A59%27%20OR%20Kommune%3D%27St%C3%A4dteregion%27%20AND%20Meldedatum%3Etimestamp%20%272020-03-16%2022%3A59%3A59%27)&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=ObjectID%2CPositiv%2CMeldedatum%2CKommune&orderByFields=Meldedatum%20asc&resultOffset=0&resultRecordCount=32000&resultType=standard&cacheHint=true"
URL2 = "https://services-eu1.arcgis.com/2ypUQspLVcN0KOBE/arcgis/rest/services/CoronavirusFallzahlen_%C3%B6ffentlich/FeatureServer/1/query?f=json&where=Kommune%3D%27Aachen%27&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Meldedatum%20desc&resultOffset=0&resultRecordCount=1&resultType=standard&cacheHint=true"
URL3 = "https://services-eu1.arcgis.com/2ypUQspLVcN0KOBE/arcgis/rest/services/CoronavirusFallzahlen_%C3%B6ffentlich/FeatureServer/1/query?f=json&where=(Kommune%3D%27Aachen%27%20AND%20Meldedatum%3Etimestamp%20%272020-03-16%2022%3A59%3A59%27%20OR%20Kommune%3D%27St%C3%A4dteregion%27%20AND%20Meldedatum%3Etimestamp%20%272020-03-16%2022%3A59%3A59%27)&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=ObjectID%2CInzidenz%2CMeldedatum%2CKommune&orderByFields=Meldedatum%20asc&resultOffset=0&resultRecordCount=32000&resultType=standard&cacheHint=true"


def do(url):
    parts = urlparse(url)
    query = parts.query
    q = parse_qs(query)

    where = q['where']
    pprint.pprint(q)
    pprint.pprint(where)


do(URL1)
print("_"*80)
do(URL3)




base_url = "https://services-eu1.arcgis.com/2ypUQspLVcN0KOBE/arcgis/rest/services/CoronavirusFallzahlen_%C3%B6ffentlich/FeatureServer/1/query?"
my_query = {
    'cacheHint': 'true',
    'f': 'json',
    'orderByFields': 'Meldedatum asc',
    'outFields': 'ObjectID,Meldedatum,Kommune',
    #'outFields': 'ObjectID,Aktiv,Tote,Neue_Tote,Inzidenz,Meldedatum,Kommune',
    'resultOffset': '0',
    'resultRecordCount': '3200',
    'resultType': 'standard',
    'returnGeometry': 'false',
    'spatialRel': 'esriSpatialRelIntersects',
    'where': "Kommune='Baesweiler' AND Meldedatum>timestamp '2020-03-16 22:59:59'"
}

newq=urlencode(my_query)
rurl = base_url+newq

print("**** GETTING")

resp = requests.get(rurl)
data = resp.json()
print(data.keys())
print(len(data['features']))
import datetime
for f in data['features']:
    d = f['attributes']
    print(datetime.datetime.fromtimestamp(d['Meldedatum']/1000))
#pprint.pprint(resp.json())

#print(rurl)


"""

## Felder

Aktiv
Genesen
Inzidenz
Kommune
Meldedatum
Neue_Fälle
Neue_Genesene
Neue_Tote
ObjectID
Positiv
Schnitt_neue_Fälle
Tote

"""