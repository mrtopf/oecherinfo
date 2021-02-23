from . import muni

def setup(api):
    """setup the api endpoints"""

    api.add_resource(
        muni.Municipality,
        '/muni/<string:muni>',
        endpoint="muni"
    )
