# oecherinfo API Proposal

## General goals

- should be easy to extend with more endpoints for more data categories (corona is not the only thing)
- you should be able to filter it down by various attributes



## versioning

In order so be able to support better ideas we will version the API.
Thus the path starts with the version number starting with `/v1/`.


## Corona

- Endpoint starts at `/v1/corona/`. We will omit this endpoint from now on. 

### Data to retrieve for graphs

- Case data per day:
    - `newCases`: new cases per day
    - `cumCases`: cumulative cases
    - `activeCases`: active cases per day
    - `rollingRate`: rolling rate per day (Inzidenz)
    - `rollingRatePerc`: change of rolling rate in percentage (like gov.uk does it **new**)
    - `avgNewCases`: average value over +/-3 days for new cases per day
    - `avgActiveCases`: average value over +/-3 days for active cases per day
    - `newDeaths`: new deaths per day
    - `avgNewDeaths`: average value over +/-3 days for deaths
    - `cumDeaths`: cumulative deaths
    - `newRecovered`: new recovered ppl per day
    - `avgNewRecovered`: average value over +/-3 days for recovered ppl
    - `cumRecovered`: cumulative recovered people

- Hospital data per day:
    - `freeBeds`: free beds per day of hospitals in the county
    - `avgFreeBeds`: average of free beds
    - `covid19Cases`: covid 19 cases in ICUs
    - `avgCovdi19Cases`: avg of covid 19 cases in ICUs
    - `ventilatorCases`: covid 19 cases on ventilators in ICUs
    - `avgVentilatorCases`: avg of covid 19 cases on ventilaros in ICUs

### Making a request

You can request any data with the following endpoints via `GET`:

- `/v1/corona/cases` to get the case data for the whole Städteregion Aachen
- `/v1/corona/hospital` to get the hospital data for the whole Städteregion Aachen

These are 2 endpoints because they have different data sources and thus also different update times. 

#### filtering by city

You can also select a specific city by appending a query parameter: `?city=aachen`.
 Use lowercase names for the cities in the Städteregion Aachen. Umlauts will be converted to `ae` etc., so use `?city=roetgen`. 

 Later we might add the possibility to add county names or identifiers as well (if we have the data).

 We use a query parameter here instead of a path so we can be more flexible e.g. in cases we want to use county names/ids. 


#### chosing attributes to return

By default all the attributes listed above will be returned by that category. In case you want to limit them you can simply use the `field=` attribute and listing them:

```
GET /v1/corona/cases?city=aachen&fields=newCases,newDeaths
```

This will return the fields `newCases` and `newDeaths` for Aachen.

The fields `date` and `city` will always be returned.

### Response

The response is in JSON and looks like follows:


```
{
    count : 71, // number of records returned
    lastUpdated: "2021-01-31T11:05:00", // date of most recent record
    result: [
        {
            date: "2020-08-05T11:05:00",
            muni: "aachen",
            newCases: 100,
            casesCumulative: 5,
        },
        {
            date: "2020-08-06T11:05:00",
            muni: "aachen",
            newCases: 89,
            casesCumulative: 2,
        },
    ]
}
```

**Question**: Should we return a list of objects or maybe just lists to save some space? It could look like this:

```
{
    count: 71,
    lastUpdated: "2020-08-05T11:05:00",
    status: {
        newCases: 99, // most recent new cases
        casesCumulative: 99, // most recent cumulative Cases
        newCasesWeekAgo: 70, // number new cases a week ago 
        cumulativeCasesWeekAgo: 70, // number new cases a week ago 
        newCasesYesterday: 97, // case count a day ago
        cumulativeCasesYesterday: 97, // cum cases a day ago

    },
    dates: [
        "2020-08-05T11:05:00",
        "2020-08-06T11:05:00",
        ...
    ],
    newCases: [
        100,
        89
    ],
    casesCumulative: [
        5,
        2,
    ],
    ...
}
```

This way we don't have to repeat the keys all the time. Moreover it might be easier to feed it into chart libraries.


### Overview data

On some graphs and on the homepage we want to display the latest data and some trends. This can be:

- the most recent value of a field
- the 7 day trend either cumulative (like for cases) or by single data point (e.g. for rolling rate where it's already an average)
- the change from the last recent value.

On oecher.info we have the following overview data right now on the homepage (plus graph data):

For rolling rate:

- date of most recent rolling rate
- most recent rolling rate
- rolling rate 7 days ago (so we can compute the change in percent and show both numbers)


For new cases:
- date of most recent new case data
- most recent count of new cases
- sum of last 7 days of new cases
- sum of next to last 7 days of new cases (again rom this we can compute the changes in percent. )


For active cases:
- date of most recent active case data
- most recent active case count
- active case count 7 days ago (to compute 7 day trend)

Moreover we have a table with all the recent data and trends for all municipalities:

- cases cumulative with trend
- rolling rate with trend
- deaths with trend
- recovered
- active cases with trend

Additionally we have the hospital status. This will be discussed later. 

Questions: 

- should we simply return a fixed set per municipality? e.g. `GET /v1/corona/status/?city=aachen`
- or should we make it configurable? Then again it's not that much data returned. For oecher.info we only need a fixed set. 
- for graph views we can simply include status data in the header. 







 









    