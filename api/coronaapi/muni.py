from flask_restful import Resource, abort, request

from corona.config import ALLOWED_MUNI_FIELDS, API_TO_DATABASE_MAPPING, DATABASE_TO_API_MAPPING
from corona.db import mongo


class Municipality(Resource):
    """return data for a municipality
    """

    def get(self, muni):
        """return data

        the following filters are allowed:

        `fields`: can be a list of fields to return. Will return all the fields if not specified
        `format`: can be `json`, `csv`, defaults to `json`

        """

        # check which fields we should return
        fields = [f.strip() for f in request.args.get('fields', '').split(",")]
        if fields == ['']:
            fields = ALLOWED_MUNI_FIELDS
        else:
            if not set(fields).issubset(set(ALLOWED_MUNI_FIELDS)):
                abort(400, message="wrong list of fields")

        # check if fields are ok
        output = request.args.get('format', 'json').lower().strip()
        if output not in ['json', 'csv']:
            abort(400, message="wrong output format, should be 'json' or 'csv'")

        # get the general header information with trends etc.

        data = list(mongo.db.data.find(
            {'municipality': muni}).sort("date", -1))
        first = data[0]
        print(data)
        resp = {
            'date': first['date'],
            'dateFormatted': first['date'].strftime("%d. %B %Y"),
            'fields': fields,
            'format': output,
        }

        today={}
        yesterday={}
        trend={}
        for f in fields:
            db_field = API_TO_DATABASE_MAPPING[f]
            today[f] = data[0][db_field]
            yesterday[f] = data[1][db_field]

        resp['today'] = today
        resp['yesterday'] = yesterday
            
        
        return resp
