import datetime
import click
import time
import requests
import csv
import io
from dateutil.parser import parse as dateparse
from urllib.parse import urlparse, parse_qs, urlencode
import pprint
from statistics import mean

from flask.cli import with_appcontext, AppGroup
from flask import current_app

from corona.db import mongo

corona_cli = AppGroup('corona')

KOMMUNEN_MAP = {
    'Städteregion': 'sr',
    'Aachen': 'aachen',
    'Alsdorf': 'alsdorf',
    'Baesweiler': 'baesweiler',
    'Eschweiler': 'eschweiler',
    'Herzogenrath': 'herzogenrath',
    'Monschau': 'monschau',
    'Roetgen': 'roetgen',
    'Simmerath': 'simmerath',
    'Stolberg': 'stolberg',
    'Würselen': 'wuerselen',
}

ATTRIBUTES = ['incidence', 'new', 'active', 'recovered', 'positive', 'deaths']


@corona_cli.command()
@with_appcontext
def import_corona():
    """import corona data"""
    start_time = time.time()

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
            '_id': oid,
            'date': datetime.datetime.fromtimestamp(d['Meldedatum']/1000),
            'municipality': KOMMUNEN_MAP[d['Kommune']],
            'municipality_name': d['Kommune'],
            'new': d['Neue_Fälle'],
            'active': d['Aktiv'],
            'recovered': d['Genesen'],
            'new_recovered': d['Neue_Genesene'],
            'incidence': d['Inzidenz'],
            'positive': d['Positiv'],
            'new_deaths': d['Neue_Tote'] or 0,
            'deaths': d['Tote'],
            'average_new_cases': d['Schnitt_neue_Fälle'],
        }

        mongo.db.data.update({'_id': oid}, record, True)
        click.echo("Import finished in %s seconds" %
                   (round(time.time()-start_time, 2)))


@corona_cli.command()
@with_appcontext
def avgs():
    """compute the 7 day averages of all features and munis"""
    start_time = time.time()

    for (name, muni) in KOMMUNEN_MAP.items():
        data = list(mongo.db.data.find({'municipality': muni}).sort("date", 1))
        for (idx, d) in enumerate(data):
            sub = data[max(idx-7, 0):idx]
            for attr in ATTRIBUTES:
                nums = [s[attr] for s in sub if s[attr] is not None]
                if len(nums) == 0:
                    m = 0
                else:
                    m = round(mean(nums))
                d["%s_avg" % attr] = m
                mongo.db.data.save(d)
        click.echo("Finished %s" % name)

    click.echo("Finished computing avgs in %s seconds" %
               (round(time.time()-start_time, 2)))


@corona_cli.command()
@with_appcontext
def import_divi():
    """import from divi register"""
    start_time = time.time()
    divi_url = "https://diviexchange.blob.core.windows.net/%24web/DIVI_Intensivregister_Auszug_pro_Landkreis.csv"
    resp = requests.get(divi_url)
    csvfile = io.StringIO(resp.text)
    #csvfile = open("example.csv", "r")
    with csvfile as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            uid = "%s-%s" %(row['gemeindeschluessel'], row['daten_stand'])
            row['date'] = dateparse(row['daten_stand'])
            row['_id'] = uid
            mongo.db.divi_daily.update({'_id': uid}, row, True)

    click.echo("Finished divi import in %s seconds" %
               (round(time.time()-start_time, 2)))


@corona_cli.command()
@with_appcontext
def import_divi_details():
    """import from divi API"""
    start_time = time.time()
    DIVI_URL = "https://www.intensivregister.de/api/public/intensivregister"
    DIVI_PARAMS = {
        'criteria': {
            'bundesland': None,
            'standortId': None,
            'standortBezeichnung': None,
            'geoSearch': { 'latitude': 50.7583, 'longitude': 6.08339, 'distanz': 30 },
            'bettenStatus': [],
            'bettenKategorie': [],
        },
        'pageNumber': 0,
        'pageSize': 7,
    }
    resp = requests.post(DIVI_URL, json=DIVI_PARAMS)
    data = resp.json()
    for hosp in data['data']:
        uid=hosp['id']
        hosp['_id'] = hosp['id']
        mongo.db.divi_hospitals.update({'_id': uid }, hosp, True)

    click.echo("Finished divi hospital import in %s seconds" %
            (round(time.time()-start_time, 2)))

@corona_cli.command()
@with_appcontext
@click.pass_context
def all(ctx):
    """import all"""
    ctx.invoke(import_corona)
    ctx.invoke(avgs)
    ctx.invoke(import_divi)
    ctx.invoke(import_divi_details)
    
