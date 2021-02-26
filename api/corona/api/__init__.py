from . import muni, divi

def setup(api):
    """setup the api endpoints"""

    api.add_resource(
        muni.Municipality,
        '/muni/<string:muni>',
        endpoint="muni"
    )
    api.add_resource(
        divi.DIVIData,
        '/divi/',
        endpoint="divi"
    )
