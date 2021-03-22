
from flask_restful import Resource, abort, request

from corona.db import mongo
from flask_csv import send_csv
import pymongo

class QuickTestData(Resource):
    """return quick test data
    """

    def get(self):
        """return data
        """

        output = request.args.get('format', 'json').lower().strip()
        if output not in ['json', 'csv']:
            abort(400, message="wrong output format, should be 'json' or 'csv'")

        sort_order = int(request.args.get("sort", "1"))
        cursor = mongo.db.quicktests.find({'county': '05334'}).sort("date",sort_order)
        if "limit" in request.args:
            limit = int(request.args.get("limit"))
            cursor = cursor.limit(limit)
        
        quicktests = list(cursor)
        
        # get the general header information with trends etc.
        today = mongo.db.quicktests.find_one({'county': '05334'}, sort=[('date', pymongo.DESCENDING)])
        date = today['date']
        today['rate_formatted'] = "%s%%" %str(round(today['rate_percent'],2)).replace(".",",")

        resp = {
            'date': date,
            'dateFormatted': date.strftime("%d. %B %Y"),
            'dates': [r['date'] for r in quicktests],
            'format': output,
            'positive': [r['positive'] for r in quicktests],
            'negative': [r['total'] - r['positive'] for r in quicktests],
            'total': [r['total'] for r in quicktests],
            'rate': [r['rate'] for r in quicktests],
            'rate_percent': [r['rate_percent'] for r in quicktests],
            'rate_permille': [r['rate_permille'] for r in quicktests],
            'today' : today
        }
        if output=="json":
            return resp
        elif output=="csv":
            headers = quicktests[-1].keys()
            return send_csv(quicktests,
                    "corona_%s_corona.csv" %(date.strftime("%Y_%m_%d")), headers)

