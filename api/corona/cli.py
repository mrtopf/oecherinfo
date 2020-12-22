import datetime
import click
import time
import requests
from urllib.parse import urlparse, parse_qs, urlencode
import pprint
from statistics import mean

from flask.cli import with_appcontext, AppGroup
from flask import current_app

from corona.db import mongo

corona_cli = AppGroup('corona')

KOMMUNEN_MAP = {
    'Städteregion' : 'sr',
    'Aachen' : 'aachen',
    'Alsdorf' : 'alsdorf',
    'Baesweiler' : 'baesweiler',
    'Eschweiler' : 'eschweiler',
    'Herzogenrath' : 'herzogenrath',
    'Monschau' : 'monschau',
    'Roetgen' : 'roetgen',
    'Simmerath' : 'simmerath',
    'Stolberg' : 'stolberg',
    'Würselen' : 'wuerselen',
}

ATTRIBUTES=['incidence', 'new', 'active', 'recovered', 'positive', 'deaths']


@corona_cli.command()
@with_appcontext
def import_corona():
    """import corona data"""
    start_time=time.time()

    my_query = {
        'cacheHint': 'true',
        'f': 'json',
        'orderByFields': 'Meldedatum asc',
        'outFields': "ObjectID, Aktiv, Genesen, Inzidenz, Kommune, Meldedatum, Neue_Fälle, Neue_Genesene, Neue_Tote, ObjectID, Positiv, Schnitt_neue_Fälle, Tote,",
        'resultOffset': '0',
        'resultRecordCount': '5200',
        'resultType': 'standard',
        'returnGeometry': 'false',
        'spatialRel': 'esriSpatialRelIntersects',
        'where': "Meldedatum>timestamp '2020-03-16 22:59:59'"
    }
    newq = urlencode(my_query)
    rurl = current_app.config['IMPORT_URL']+newq

    resp = requests.get(rurl)
    data = resp.json()
    for f in data['features']:
        d = f['attributes']
        
        oid = d['ObjectID']
        record = {
            '_id' : oid,
            'date' : datetime.datetime.fromtimestamp(d['Meldedatum']/1000),
            'municipality': KOMMUNEN_MAP[d['Kommune']],
            'municipality_name': d['Kommune'],
            'new' : d['Neue_Fälle'],
            'active' : d['Aktiv'],
            'recovered' : d['Genesen'],
            'new_recovered' : d['Neue_Genesene'],
            'incidence' : d['Inzidenz'],
            'positive' : d['Positiv'],
            'new_deaths' : d['Neue_Tote'] or 0,
            'deaths' : d['Tote'],
            'average_new_cases' : d['Schnitt_neue_Fälle'],
        }
    
        mongo.db.data.update({'_id': oid}, record, True)
        click.echo("Import finished in %s seconds" %(round(time.time()-start_time,2)))



@corona_cli.command()
@with_appcontext
def avgs():
    """compute the 7 day averages of all features and munis"""
    start_time=time.time()

    for (name,muni) in KOMMUNEN_MAP.items():
        data = list(mongo.db.data.find({'municipality': muni}).sort("date", 1))
        for (idx, d) in enumerate(data):
            sub = data[max(idx-7,0):idx]
            for attr in ATTRIBUTES:
                nums = [s[attr] for s in sub if s[attr] is not None]
                if len(nums)==0:
                    m = 0
                else:
                    m = round(mean(nums))
                d["%s_avg" %attr]= m
                mongo.db.data.save(d)
        click.echo("Finished %s" %name)
        
    click.echo("Finished computing avgs in %s seconds" %(round(time.time()-start_time,2)))
