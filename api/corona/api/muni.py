
from flask_restful import Resource, abort, request

from corona.config import ALLOWED_MUNI_FIELDS, API_TO_MUNI_DATABASE_MAPPING
from corona.db import mongo

from flask_csv import send_csv


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
            {'municipality': muni, 'r4': {'$exists': True}}).sort("date", -1))
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

        # put everything in today and yesterday
        for f in ALLOWED_MUNI_FIELDS:
            db_field = API_TO_MUNI_DATABASE_MAPPING[f]
            if data[0][db_field]:
                today[f] = round(data[0][db_field],0 if f=='rollingRate' else 2)
            else:
                today[f] = None
            if data[1][db_field]:
                yesterday[f] = round(data[1][db_field],0 if f=='rollingRate' else 2)
            else:
                yesterday[f] = None

        for f in fields:
            db_field = API_TO_MUNI_DATABASE_MAPPING[f]

            # add the series to the response
            if f == "rollingRate":
                series = resp[f] = [round(d[db_field] or 0,0) for d in data]
            else:
                series = resp[f] = [round(d[db_field] or 0,2) for d in data]
            resp[f].reverse()

            # compute the trends
            if f=="rollingRate":
                diff = trend['rollingRate7DayChange'] = round(data[0]['incidence'] - max(data[7]['incidence'],1),2)
                trend['rollingRate7DayChangePercent'] = round(diff / data[7]['incidence'],2)
            elif f.startswith("cum"):
                # we assume cumulative data here
                # we sum the values of the last 7 days and the 7 days before that
                last7 = trend['%s7DaySum' %f] = series[-1] - series[-8]
                last14 = trend['%s14DaySum' %f] = series[-8] - series[-14] # change in previous week
                diff = trend['%s7DayChange' %f] = last7 - last14
                trend['%s7DayChangePercent' %f] = round(diff / max(last7,1),2)
            else:
                # here we just take the value from 7 days back
                last7 = trend['%s7DaySum' %f] = series[-8]
                diff = trend['%s7DayChange' %f] = series[-1] - series[-8]
                trend['%s7DayChangePercent' %f] = round(diff / max(last7,1),2)

                
        resp['today'] = today
        resp['yesterday'] = yesterday
        resp['trend'] = trend
        if output=="json":
            return resp
        elif output=="csv":
            headers = ['date'] + fields
            res = []
            for (idx, d) in enumerate(resp['dates']):
                record = dict([(f, resp[f][idx]) for f in fields])
                record['date'] = d.date()
                res.append(record)
            return send_csv(res,
                    "corona_%s_%s_corona.csv" %(resp['date'].strftime("%Y_%m_%d"), muni), headers)