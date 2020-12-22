

# oecher.info website

This is the repository which powers https://oecher.info which is providing corona information
for the city of Aachen/Germany and the surrounding area.


## Requirements

- MongoDB
- Python3
- node.js




## Setup

Create a python venv with

```
python3 -m venv .
source bin/activate
```

Install packages:

```
pip install -r requirements.txt
cd api
python setup.py develop
``` 

Serve via `start.sh`

Adjust `api/etc/dev.ini` accordingly for ports etc.

## frontend setup

```
cd frontend
yarn
yarn serve
```

Adjust .env.development accordingly.


use yalc to add annotations for chart.js

The annotation plugin is unreleased as we use chart.js 3.0.0b7 or so. Thus we need to add it ourselves and
this can be done via yalc. 

See https://www.viget.com/articles/how-to-use-local-unpublished-node-packages-as-project-dependencies/
