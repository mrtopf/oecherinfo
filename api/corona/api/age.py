
from flask_restful import Resource, abort, request

from corona.db import mongo



class AgeData(Resource):
    """return age incidence data
    """

    def get(self):
        """return data
        """

        # get the general header information with trends etc.
        data = mongo.db.age_incidence.find_one({'_id': '05334'})
        return data


