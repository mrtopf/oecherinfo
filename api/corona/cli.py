import datetime
from typing import NoReturn
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

import pandas
import math
import zeep

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

# all attributes we compute averages for
ATTRIBUTES = ['incidence', 'new', 'active', 'new_recovered',
              'new_deaths', 'recovered', 'positive', 'deaths']
# ATTRIBUTES = ['incidence', 'new', 'active', 'new_recovered', 'new_deaths']
ATTRIBUTES_DIVI = ['faelle_covid_aktuell', 'faelle_covid_aktuell_beatmet',
                   'betten_frei', 'betten_belegt', 'betten_gesamt']


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
        doc = mongo.db.data.find_one({'_id': oid})
        if doc is None:
            doc = {}
        doc.update({
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
        })

        mongo.db.data.update({'_id': oid}, doc, True)
        click.echo("Import finished in %s seconds" %
                   (round(time.time()-start_time, 2)))


@corona_cli.command()
@with_appcontext
def avgs():
    """compute
        - the 7 day averages of all features in
        - the change per day

        We compute a 7 day window around the number (+/-3)

        Naming:
            - `feature_avg` is the rolling average
            - `feature_change` is the change from last day
    """
    start_time = time.time()
    window_size = 7

    for (name, muni) in KOMMUNEN_MAP.items():
        data = list(mongo.db.data.find({'municipality': muni}).sort("date", 1))

        cases = [0 if d['new'] is None else d['new'] for d in data]

        ###
        # compute R4 and R7
        ###
        window = 4
        # note that a[:len(cases)] does not get the last element
        for t in range(0, len(cases)+1):
            if t < window*2:
                data[t-1]['r4'] = None
            else:
                data[t-1]['r4'] = round(sum(cases[t-window:t]) /
                                        max(sum(cases[t-window*2:t-window]), 1), 2)
            mongo.db.data.save(data[t-1])

        window = 7
        for t in range(0, len(cases)+1):
            if t < window*2:
                data[t-1]['r7'] = None
            else:
                data[t-1]['r7'] = round(sum(cases[t-window:t]) /
                                        max(sum(cases[t-window*2:t-window]), 1), 2)
                # print(data[t-1]['r7'], data[t-1]['new'])
            mongo.db.data.save(data[t-1])

        for attr in ATTRIBUTES:
            numbers = [d[attr] for d in data]
            numbers_series = pandas.Series(numbers)
            windows = numbers_series.rolling(window_size, center=True)
            moving_averages = windows.mean()

            # convert nan to None
            avg = [None if math.isnan(d) else d for d in moving_averages]

            # put data back into individual records in data
            for idx, v in enumerate(avg):
                data[idx][attr+'_avg'] = v

                # get yesterdays value
                # not sure we really need this as we only need it for status
                if idx > 0:
                    data[idx][attr+'_last'] = data[idx-1][attr]
                else:
                    data[idx][attr+'_last'] = data[idx][attr]

                # for incidence compute percentage change from past 7 days
                if attr == "incidence":
                    # incidence should not be None or 0 (div by zero)
                    if idx > 7 and data[idx-7]['incidence']:
                        diff = data[idx]['incidence'] - \
                            data[idx-7]['incidence']
                        perc = diff/data[idx-7]['incidence']
                    else:
                        perc = 0
                    data[idx]['incidence_perc'] = perc
                    data[idx]['incidence_perc_100'] = round(perc*100)

                mongo.db.data.save(data[idx])

        click.echo("Finished %s" % name)

    # do divi averages
    data = list(mongo.db.divi_daily.find(
        {'gemeindeschluessel': '05334'}).sort("date", 1))
    # compute beds sum
    for idx, d in enumerate(data):
        data[idx]['betten_gesamt'] = int(
            d['betten_frei']) + int(d['betten_belegt'])
        for attr in ATTRIBUTES_DIVI:
            data[idx][attr] = int(data[idx][attr])

    for attr in ATTRIBUTES_DIVI:
        numbers = [d[attr] for d in data]
        numbers_series = pandas.Series(numbers)
        windows = numbers_series.rolling(window_size, center=True)
        moving_averages = windows.mean()

        # convert nan to None
        avg = [None if math.isnan(d) else d for d in moving_averages]

        # put data back into individual records in data
        for idx, v in enumerate(avg):
            data[idx][attr+'_avg'] = v
            mongo.db.divi_daily.save(data[idx])

        click.echo("Finished DIVI - %s" % attr)

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
    with csvfile as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            uid = "%s-%s" % (row['gemeindeschluessel'], row['daten_stand'])
            row['date'] = dateparse(row['daten_stand'])
            row['_id'] = uid
            if "faelle_covid_aktuell_invasiv_beatmet" in row:
                row['faelle_covid_aktuell_beatmet'] = row['faelle_covid_aktuell_invasiv_beatmet']
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
            'geoSearch': {'latitude': 50.7583, 'longitude': 6.08339, 'distanz': 30},
            'bettenStatus': [],
            'bettenKategorie': [],
        },
        'pageNumber': 0,
        'pageSize': 7,
    }
    resp = requests.post(DIVI_URL, json=DIVI_PARAMS)
    data = resp.json()
    for hosp in data['data']:
        uid = hosp['krankenhausStandort']['id']
        hosp['_id'] = uid

        hosp['bettenStatus'] = {
            "statusLowCare" : hosp['maxBettenStatusEinschaetzungLowCare'],
		    "statusHighCare" : hosp['maxBettenStatusEinschaetzungHighCare'],
		    "statusECMO" : hosp['maxBettenStatusEinschaetzungEcmo'],
        }
        date = hosp['date'] = datetime.datetime.now()
        hosp['dateFormatted'] = date.strftime("%d. %B %Y")
        
        mongo.db.divi_hospitals.update({'_id': uid}, hosp, True)

    click.echo("Finished divi hospital import in %s seconds" %
               (round(time.time()-start_time, 2)))


@corona_cli.command()
@with_appcontext
@click.argument('filename')
def import_quicktests(filename):
    """import the quick test data from a CSV file"""
    start_time = time.time()

    with open(filename, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            date = row['date'] = dateparse(row['date'])
            uid = row['_id'] = "sr-%s" %(date.strftime("%d.%m.%Y"))
            row['county']="05334"
            total = row['total'] = int(row['total'])
            positive = row['positive'] = int(row['positive'])
            row['rate'] = positive/total
            row['rate_percent'] = round(positive/total*100,2)
            row['rate_permille'] = round(positive/total*1000,2)
            mongo.db.quicktests.update({'_id': uid}, row, True)
    click.echo("Finished self test data import in %s seconds" %
               (round(time.time()-start_time, 2)))



@corona_cli.command()
@with_appcontext
def import_age_groups():
    """import from SurvStat+

    this code is taken from

    https://github.com/rgieseke/opencoviddata

    and adapted for our needs.


    """
    from .coronaimport.survstat import import_age_incidence, import_age_sex

    start_time = time.time()
    import_age_incidence()
    import_age_sex()

    click.echo("Finished age group import in %s seconds" %
               (round(time.time()-start_time, 2)))



@corona_cli.command()
@with_appcontext
@click.pass_context
def all(ctx):
    """import all"""
    ctx.invoke(import_corona)
    ctx.invoke(import_divi)
    ctx.invoke(import_divi_details)
    ctx.invoke(avgs)
    ctx.invoke(import_age_groups)
