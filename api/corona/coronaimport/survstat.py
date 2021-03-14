import datetime
from urllib.parse import DefragResultBytes

from corona.db import mongo
from .common import SurvStatRequest


def toFloat(x):
    """convert a localized string to float"""
    if x=="" or x is None:
        return 0
    return float(x.replace(".","").replace(",","."))

def import_age_incidence():
    """import the age groups by incidence and week"""

    req = SurvStatRequest()
    response = req(
        {
            "ColumnHierarchy": "[ReportingDate].[YearWeek]",
            "RowHierarchy": "[AlterPerson80].[AgeGroupName6]",
        }
    )

    columns = req.columns
    dates = [datetime.datetime.strptime(
        d + '-1', "%Y-KW%W-%w") for d in columns]

    result = {'_id': req.COUNTY['County'],
              'weeks': dates,
              'updated': datetime.datetime.now()}

    groups = {}
    for row in response.QueryResults.QueryResultRow:
        if row['Caption'] == "Gesamt":
            continue
        nums = [float(i.replace(
            ".", "").replace(',', '.')) if i is not None else 0 for i in row['Values']['string'][1:]]
        label = row['Caption'][1:].replace("..", "-")
        groups[label] = nums
        # print(nums)
        #print(row['Caption'], row['Values']['string'])

    result['groups'] = groups
    mongo.db.age_incidence.update({'_id': req.COUNTY['County']}, result, True)


def import_age_sex():
    """import the age and sex distribution

    ctl00$ctl00$ContentPlaceHolderMain$ContentPlaceHolderAltGridFull$DropDownListRowHierarchy: [Geschlecht].[SortGruppe]
    ctl00$ctl00$ContentPlaceHolderMain$ContentPlaceHolderAltGridFull$DropDownListColHierarchy: [AlterPerson80].[AgeGroupName6]
    """

    # get rates
    req = SurvStatRequest()
    response = req(
        {
            "ColumnHierarchy": "[AlterPerson80].[AgeGroupName6]",
            "RowHierarchy": "[Geschlecht].[SortGruppe]",
        }
    )

    columns = req.columns
    result = {'_id': req.COUNTY['County'],
              'labels': columns,
              'updated': datetime.datetime.now()}

    for row in response.QueryResults.QueryResultRow:
        data = [toFloat(a) for a in row['Values']['string']]
        if row['Caption']=="männlich":
            k = "male_rate"
        elif row['Caption']=="weiblich":
            k = "female_rate"
        else:
            k = "total_rate"
        result[k] = data


    # get numbers
    req = SurvStatRequest(incidence=False)
    response = req(
        {
            "ColumnHierarchy": "[AlterPerson80].[AgeGroupName6]",
            "RowHierarchy": "[Geschlecht].[SortGruppe]",
        }
    )

    for row in response.QueryResults.QueryResultRow:
        data = [toFloat(a) for a in row['Values']['string']]
        if row['Caption']=="männlich":
            k = "male"
        elif row['Caption']=="weiblich":
            k = "female"
        elif row['Caption']=="unbekannt":
            k = "unknown"
        elif row['Caption']=="divers":
            k = "diverse"
        else:
            k = "total"
        result[k] = data[1:]


    mongo.db.age_sex.update({'_id': req.COUNTY['County']}, result, True)
