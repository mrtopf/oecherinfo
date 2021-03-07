MUNI_DATABASE_TO_API_MAPPING = {
    "new" : 'newCases',
	"active" : 'activeCases',
	"recovered" : 'cumRecovered',
	"new_recovered" : 'newRecovered',
	"incidence" : 'rollingRate',
	"positive" : 'cumCases',
	"new_deaths" : 'newDeaths',
	"deaths" : 'cumDeaths',
	"r4" : 'r4',
	"r7" : 'r7',
	"incidence_avg" : 'avgRollingRate',
	"incidence_perc" : 'rollingRatePerc',
	"new_avg" : 'avgNewCases',
	"active_avg" : 'avgActiveCases',
	"new_recovered_avg" : 'avgNewRecovered',
	"new_deaths_avg" : 'avgNewDeaths',
}

API_TO_MUNI_DATABASE_MAPPING = {v: k for k, v in MUNI_DATABASE_TO_API_MAPPING.items()}

ALLOWED_MUNI_FIELDS = list(API_TO_MUNI_DATABASE_MAPPING.keys())



DIVI_DATABASE_TO_API_MAPPING = {
    "faelle_covid_aktuell" : "covid19Cases",
	"faelle_covid_aktuell_avg" : "avgCovid19Cases",
	"faelle_covid_aktuell_beatmet" : "ventilatorCases",
	"faelle_covid_aktuell_beatmet_avg" : "avgVentilatorCases",
	"betten_frei" : "freeBeds",
	"betten_frei_avg" : "avgFreeBeds",
	"betten_belegt" : "occupiedBeds",
	"betten_belegt_avg" : "avgOccupiedBeds",
	"betten_gesamt" : "allBeds",
	"betten_gesamt_avg" : "avgAllBeds"
}

API_TO_DIVI_DATABASE_MAPPING = {v: k for k, v in DIVI_DATABASE_TO_API_MAPPING.items()}

ALLOWED_DIVI_FIELDS = list(API_TO_DIVI_DATABASE_MAPPING.keys())
