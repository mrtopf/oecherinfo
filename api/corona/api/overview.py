
from flask_restful import Resource, abort, request

from corona.config import ALLOWED_MUNI_FIELDS, API_TO_MUNI_DATABASE_MAPPING

from corona.db import mongo

MUNIS = [
    {"muni": "aachen", "name": "Aachen"},
    {"muni": "alsdorf", "name": "Alsdorf"},
    {"muni": "baesweiler", "name": "Baesweiler"},
    {"muni": "eschweiler", "name": "Eschweiler"},
    {"muni": "herzogenrath", "name": "Herzogenrath"},
    {"muni": "monschau", "name": "Monschau"},
    {"muni": "roetgen", "name": "Roetgen"},
    {"muni": "simmerath", "name": "Simmerath"},
    {"muni": "stolberg", "name": "Stolberg"},
    {"muni": "wuerselen", "name": "Würselen"},
    {"muni": "sr", "name": "Städteregion Aachen"},
]

class Overview(Resource):
    """return overview data for muni table
    """

    def get(self):
        """return status data for all munis
        """

        resp= []
        for muni in MUNIS:
            record= {
                'muni': muni['muni'],
                'name': muni['name'],
            }
            data=  list(mongo.db.data.find({'municipality': muni['muni'], 'r4': {'$exists': True}}).sort("date", -1).limit(20))
            today={}
            yesterday={}
            trend={}

            # put everything in today and yesterday
            for f in ALLOWED_MUNI_FIELDS:
                db_field = API_TO_MUNI_DATABASE_MAPPING[f]

                if f == "rollingRate":
                    series = [round(d[db_field] or 0,0) for d in data]
                else:
                    series = [round(d[db_field] or 0,2) for d in data]

                if data[0][db_field]:
                    today[f] = round(data[0][db_field],0 if f=='rollingRate' else 2)
                else:
                    today[f] = None
                if data[1][db_field]:
                    yesterday[f] = round(data[1][db_field],0 if f=='rollingRate' else 2)
                else:
                    yesterday[f] = None
                
                # compute the trends
                if f=="rollingRate":
                    diff = trend['rollingRate7DayChange'] = round(data[0]['incidence'] - data[7]['incidence'],2)
                    trend['rollingRate7DayChangePercent'] = round(diff / max(data[7]['incidence'],1),2)
                elif f.startswith("cum"):
                    # we assume cumulative data here
                    # we sum the values of the last 7 days and the 7 days before that
                    last7 = trend['%s7DaySum' %f] = series[-1] - series[-8]
                    last14 = trend['%s14DaySum' %f] = series[-9] - series[-15] # change in previous week
                    diff = trend['%s7DayChange' %f] = last7 - last14
                    trend['%s7DayChangePercent' %f] = round(diff / max(last7,0.0001),2)
                else:
                    # here we just take the value from 7 days back
                    last7 = trend['%s7DaySum' %f] = series[-8]
                    diff = trend['%s7DayChange' %f] = series[-1] - series[-8]
                    trend['%s7DayChangePercent' %f] = round(diff / max(last7,0.0001),2)

                    
            record['today'] = today
            record['yesterday'] = yesterday
            record['trend'] = trend
            resp.append(record)
        return resp



        for f in ALLOWED_MUNI_FIELDS:
            db_field= API_TO_MUNI_DATABASE_MAPPING[f]
            if data[0][db_field]:
                today[f]= round(data[0][db_field], 0 if f == 'rollingRate' else 2)
            else:
                today[f]= None
            if data[1][db_field]:
                yesterday[f]= round(data[1][db_field], 0 if f == 'rollingRate' else 2)
            else:
                yesterday[f]= None

        return resp
