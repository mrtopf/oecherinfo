from . import muni, divi, overview

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

    api.add_resource(
        overview.Overview,
        '/overview/',
        endpoint="overview"
    )
