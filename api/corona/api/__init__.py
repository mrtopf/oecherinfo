from . import muni, divi, overview, age

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
        age.AgeData,
        '/age/',
        endpoint="age"
    )

    api.add_resource(
        overview.Overview,
        '/overview/',
        endpoint="overview"
    )
