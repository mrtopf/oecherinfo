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
#ATTRIBUTES = ['incidence', 'new', 'active', 'new_recovered', 'new_deaths']
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
                #print(data[t-1]['r7'], data[t-1]['new'])
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
        uid = hosp['id']
        hosp['_id'] = hosp['id']
        mongo.db.divi_hospitals.update({'_id': uid}, hosp, True)

    click.echo("Finished divi hospital import in %s seconds" %
               (round(time.time()-start_time, 2)))


"""
this is obtained from survstart via a curl url obtained by creating the query at

https://survstat.rki.de/Content/Query/Create.aspx

The script is available as `get_age_group.sh`

This will put a zip file into a temp directory to read

"""


@corona_cli.command()
@with_appcontext
def import_age_groups():
    """import from SurvStat+

    this code is taken from

    https://github.com/rgieseke/opencoviddata

    and adapted for our needs.


    """
    start_time = time.time()

    client = zeep.Client(
        "https://tools.rki.de/SurvStat/SurvStatWebService.svc?wsdl")
    factory = client.type_factory("ns2")
    county = {"State": "05", "Region": "DEA2", "County": "05334"}

    res = client.service.GetOlapData(
        {
            "Language": "German",
            "Measures": {"Incidence": 1},
            "Cube": "SurvStat",
            # Totals still included, setting `true` yields duplicates
            "IncludeTotalColumn": False,
            "IncludeTotalRow": False,
            "IncludeNullRows": False,
            "IncludeNullColumns": False,
            "HierarchyFilters": factory.FilterCollection(
                [
                    {
                        "Key": {
                            "DimensionId": "[PathogenOut].[KategorieNz]",
                            "HierarchyId": "[PathogenOut].[KategorieNz].[Krankheit DE]",
                        },
                        "Value": factory.FilterMemberCollection(
                            ["[PathogenOut].[KategorieNz].[Krankheit DE].&[COVID-19]"]
                        ),
                    },
                    {
                        "Key": {
                            "DimensionId": "[ReferenzDefinition]",
                            "HierarchyId": "[ReferenzDefinition].[ID]",
                        },
                        "Value": factory.FilterMemberCollection(
                            ["[ReferenzDefinition].[ID].&[1]"]
                        ),
                    },
                    {
                        "Key": {
                            "DimensionId": "[DeutschlandNodes].[Kreise71Web]",
                            "HierarchyId": "[DeutschlandNodes].[Kreise71Web].[FedStateKey71]",
                        },
                        "Value": factory.FilterMemberCollection(
                            [
                                f"[DeutschlandNodes].[Kreise71Web].[FedStateKey71].&[{ county['State'] }].&[{ county['Region'] }].&[{ county['County'] }]"
                            ]
                        ),
                    },
                ]
            ),
            "ColumnHierarchy": "[ReportingDate].[YearWeek]",
            "RowHierarchy": "[AlterPerson80].[AgeGroupName6]",
        }
    )

    # convert 2020-KW1 etc. in dates
    now = datetime.datetime.now()
    start = datetime.datetime(year=2020, month=3, day=1)
    columns = [i["Caption"] for i in res.Columns.QueryResultColumn[1:]]
    dates = [datetime.datetime.strptime(
        d + '-1', "%Y-KW%W-%w") for d in columns]

    result = {'_id': county['County'],
              'weeks': dates,
              'updated': datetime.datetime.now()}

    groups = {}
    for row in res.QueryResults.QueryResultRow:
        if row['Caption'] == "Gesamt":
            continue
        nums = [float(i.replace(
            ".", "").replace(',', '.')) if i is not None else 0 for i in row['Values']['string'][1:]]
        label = row['Caption'][1:].replace("..", "-")
        groups[label] = nums
        # print(row['Caption'], row['Values']['string'])

    result['groups'] = groups
    mongo.db.age_incidence.update({'_id': county['County']}, result, True)

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
