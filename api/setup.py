from setuptools import setup

setup(
    name='corona',
    version='1.1',
    url="https://comlounge.net",
    packages=['corona'],
    author="COM.lounge GmbH",
    author_email="info@comlounge.net",
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'gunicorn',
        'click',
        'flask',
        'flask-restful',
        'flask-pymongo',
        'flask-mongoengine',
        'Flask-Cors',
    ],
    entry_points={
        'flask.commands': [
            'corona=corona.cli:corona_cli'
        ],
    },
    tests_require=[
    ]
)
