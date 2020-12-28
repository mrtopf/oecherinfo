import datetime

import locale
locale.setlocale(locale.LC_TIME, "de_DE") 

from flask import Flask, json
from flask_cors import CORS
from flask_restful import Api

from flask_restful import Resource, abort, request

from corona.db import mongo
from corona.json_encoder import CustomJSONEncoder

FIELDS = [
    "new",
    "active",
    "recovered",
    "new_recovered",
    "incidence",
    "positive",
    "new_deaths",
    "deaths",
    "average_new_cases",
    "new_avg",
    "active_avg",
    "recovered_avg",
    "incidence_avg",
    "positive_avg",
    "deaths_avg",
]

HOSPITAL_MAP = {
    '771888' :  'Marienhospital, Aachen',
    '772078' :  'Luisenhospital, Aachen',
    '771450' :  'Universitätsklinikum, Aachen',
    '772113' :  'Rhein-Maas Klinikum, Würselen',
    '771699' :  'Bethlehem-Gesundheitszentrum, Stolberg',
    '772187' :  'St.-Antonius-Hospital, Eschweiler',
    '772720' :  'Eifelklinik St. Brigida, Simmerath',
}

STATUS_COLORS = {
    'NICHT_VERFUEGBAR': 'red',
    'BEGRENZT': 'oecheryellow',
    'KEINE_ANGABE': 'grey lighten-3',
    'VERFUEGBAR': 'green',
}

class MuniData(Resource):
    """return data for one municipality"""

    def get(self, muni):
        """return data for a muni and a number of fields

        fields will be passed via query arg

        fields need to be comma separated.

        will return a dictionary with `labels` and all the fields
        as separate keys

        """

        labels = []
        data = {}

        for field in FIELDS:
            data[field] = []

        results =  mongo.db.data.find({'municipality': muni}).sort("date", 1)
        for item in results:
            labels.append(item['date'].strftime("%d. %b"))
            for field in FIELDS:
                data[field].append(item[field])
        return {
            'labels' : labels,
            'data' : data
        }
            
class AllData(Resource):
    """return base information about the corona situation:

    for last known date: 
        - the date
        - new cases in each muni for today
        - incidence in each muni
        - deaths in each muni
        - recovered in each muni
        - active in each muni

    We also return the data for each muni as

    {
        <muni_name> : {
            labels: [....],
            active: [....]
        }
    }
    """

    def get(self):
        """
        """

        results =  mongo.db.data.find().sort("date", -1).limit(1)[0]
        resp = {
            'date' : results['date'],
            'dateFormatted' : results['date'].strftime("%d. %B %Y"),
        }

        yesterdate = results['date'] - datetime.timedelta(hours=24)
        weekerdate = results['date'] - datetime.timedelta(hours=24*7) # a week ago
        resp['yesterdate'] = yesterdate
        resp['yesterdateFormatted'] = yesterdate.strftime("%d. %B %Y")
        results = mongo.db.data.find({'date': results['date']})
        yd_results = mongo.db.data.find({'date': yesterdate})
        wd_results = mongo.db.data.find({'date': weekerdate})
        munis = {}
        today_data = {}
        yesterday_data = {}
        weekerday_data = {}
        for rec in results:
            m = rec['municipality']
            munis[m] = rec['municipality_name']
            today_data[m] = rec
        for rec in yd_results:
            m = rec['municipality']
            yesterday_data[m] = rec
        for rec in wd_results:
            m = rec['municipality']
            weekerday_data[m] = rec
        resp['munis'] = munis
        resp['today'] = today_data
        resp['yesterday'] = yesterday_data
        resp['weekerday'] = weekerday_data

        # now get old data per municipality
        muni_data = {}
        for muni in munis: 
            data = dict([(f, []) for f in FIELDS+['labels']])
            results =  mongo.db.data.find({'municipality': muni}).sort("date", 1)
            for rec in results:
                data['labels'].append(rec['date'])#.strftime("%d. %b"))
                for field in FIELDS:
                    data[field].append(rec[field] or 0)
            muni_data[muni] = data
            
        resp['muni_data'] = muni_data

        # add divi data
        divi_results =  mongo.db.divi_daily.find({'gemeindeschluessel': '05334'}).sort("date", -1).limit(1)[0]
        resp['divi'] = divi_results
        resp['divi']['dateFormatted'] = resp['divi']['date'].strftime("%d.%m.%Y %H:%M")

        # get hospitals
        divi_results =  mongo.db.divi_hospitals.find({},{'krankenhausStandort': 1, 'bettenStatus': 1})
        hospitals = []
        for h in divi_results:
            hospitals.append({
                #'name': h['krankenhausStandort']['bezeichnung'],
                'name': HOSPITAL_MAP[h['_id']],
                'lowCare': STATUS_COLORS[h['bettenStatus']['statusLowCare']],
                'highCare': STATUS_COLORS[h['bettenStatus']['statusHighCare']],
                'ecmo': STATUS_COLORS[h['bettenStatus']['statusECMO']],
                'lowCareText': h['bettenStatus']['statusLowCare'].capitalize(),
                'highCareText': h['bettenStatus']['statusHighCare'].capitalize(),
                'ecmoText': h['bettenStatus']['statusECMO'].capitalize(),
                
            })
    
        resp['hospitals'] = hospitals
        return resp

            

def create_app(config=None):
    """initialize the API"""

    app = Flask("corona")

    app.config.update(dict(
        DEBUG=True,
        TESTING=True,
        MONGODB_DB="corona",
        MONGODB_HOST="127.0.0.1",
        MONGO_URI="mongodb://localhost/corona",
        SECRET_KEY="c8d9c7s9d87cg9sd897dsbs789cd790b8cbd7980b9sd870cb789dc",
        RESTFUL_JSON={'cls': CustomJSONEncoder},
        IMPORT_URL="https://services-eu1.arcgis.com/2ypUQspLVcN0KOBE/arcgis/rest/services/CoronavirusFallzahlen_%C3%B6ffentlich/FeatureServer/1/query?"
    ))
    app.config.update(config or {})


    try:
        app.config.from_envvar('CORONA_SETTINGS')
    except RuntimeError:
        # env var was not set, so ignore
        pass

    CORS(app, supports_credentials=True)
    mongo.init_app(app)

    from corona import cli
    app.cli.add_command(cli.corona_cli)

    # REST endpoints

    api = Api(app, prefix='/api')
    api.add_resource(
        MuniData,
        '/muni/<string:muni>',
        endpoint="muni_data"
    )
    api.add_resource(
        AllData,
        '/all',
        endpoint="all"
    )

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=5501, host="0.0.0.0", threaded=True, use_reloader=True)