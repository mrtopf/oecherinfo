
from flask_restful import Resource, abort, request

from corona.config import API_TO_DIVI_DATABASE_MAPPING, ALLOWED_DIVI_FIELDS
from corona.db import mongo


STATUS_COLORS = {
    'NICHT_VERFUEGBAR': 'red',
    'BEGRENZT': 'oecheryellow',
    'KEINE_ANGABE': 'grey lighten-3',
    'VERFUEGBAR': 'green',
}


HOSPITAL_MAP = {
    '771888' :  'Marienhospital, Aachen',
    '772078' :  'Luisenhospital, Aachen',
    '771450' :  'Universitätsklinikum, Aachen',
    '772113' :  'Rhein-Maas Klinikum, Würselen',
    '771699' :  'Bethlehem-Gesundheitszentrum, Stolberg',
    '772187' :  'St.-Antonius-Hospital, Eschweiler',
    '772720' :  'Eifelklinik St. Brigida, Simmerath',
}



class DIVIData(Resource):
    """return divi data for hospitals
    """

    def get(self):
        """return data

        the following filters are allowed:

        `fields`: can be a list of fields to return. Will return all the fields if not specified
        `format`: can be `json`, `csv`, defaults to `json`

        """

        # check which fields we should return
        fields = [f.strip() for f in request.args.get('fields', '').split(",")]
        if fields == ['']:
            fields = ALLOWED_DIVI_FIELDS
        else:
            if not set(fields).issubset(set(ALLOWED_DIVI_FIELDS)):
                abort(400, message="wrong list of fields")

        # check if fields are ok
        output = request.args.get('format', 'json').lower().strip()
        if output not in ['json', 'csv']:
            abort(400, message="wrong output format, should be 'json' or 'csv'")

        
        # get the general header information with trends etc.
        data = list(mongo.db.divi_daily.find(
            {'gemeindeschluessel': '05334'}).sort("date", -1))
        first = data[0]
        resp = {
            'date': first['date'],
            'dateFormatted': first['date'].strftime("%d. %B %Y"),
            'fields': fields,
            'format': output,
            'dates': list(reversed([d['date'] for d in data]))
        }        
    
        today={}
        yesterday={}
        trend={}
        for f in fields:
            db_field = API_TO_DIVI_DATABASE_MAPPING[f]
            if data[0][db_field]:
                today[f] = round(float(data[0][db_field]),0)
            else:
                today[f] = None
            if data[1][db_field]:
                yesterday[f] = round(float(data[1][db_field]),0)
            else:
                yesterday[f] = None

            # add the series to the response
            series = resp[f] = [round(float(d[db_field] or 0),0) for d in data]
            resp[f].reverse()

            # compute the trends
            diff = trend['%s7DayChange' %f] = sum(series[0:7]) - sum(series[8:14])
            trend['%s7DayChangePercent' %f] = round(diff / max(sum(series[8:14]),0.0001),2)

        # add hospital status
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

                
        resp['today'] = today
        resp['yesterday'] = yesterday
        resp['trend'] = trend

        return resp
