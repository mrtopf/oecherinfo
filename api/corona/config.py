DATABASE_TO_API_MAPPING = {
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

API_TO_DATABASE_MAPPING = {v: k for k, v in DATABASE_TO_API_MAPPING.items()}

ALLOWED_MUNI_FIELDS = list(API_TO_DATABASE_MAPPING.keys())