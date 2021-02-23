



from flask_restful import Resource, abort, request

class Overview(Resource):
    """return most recent data and trends
    """

    def get(self):
        """return data"""

        return {

        }