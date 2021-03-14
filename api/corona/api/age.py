
from flask_restful import Resource, abort, request

from corona.db import mongo



class AgeData(Resource):
    """return age incidence data
    """

    def get(self):
        """return data
        """

        # get the general header information with trends etc.
        incidence = mongo.db.age_incidence.find_one({'_id': '05334'})
        age_sex = mongo.db.age_sex.find_one({'_id': '05334'})
        return {
            'incidence': incidence,
            'age_sex': age_sex,
        }


