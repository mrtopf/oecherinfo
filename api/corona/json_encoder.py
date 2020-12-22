from json import JSONEncoder
import datetime
import bson


class CustomJSONEncoder(JSONEncoder):
    """custom json encoder with extra project specific functionality

    This json encoder is used to encode the responses of the request handlers
    to JSON. We need this to properly encode project specific model class
    objects like `ObjectId`.
    """

    def default(self, o):
        if isinstance(o, datetime.datetime):
            # convert `datetime` objects to iso format
            return o.isoformat()
        elif isinstance(o, bson.ObjectId):
            # convert mongo's `ObjectId` objects to `string`
            return str(o)
        else:
            # convert list of objects to a list of their JSON compatible
            # representations
            try:
                iter(o)
            except TypeError:
                pass
            else:
                return [self.default(i) for i in o]
        # Let the base class default method raise the TypeError
        return JSONEncoder.default(self, o)
