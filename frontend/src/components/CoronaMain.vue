<template>
    <v-container fluid class="pa-0">
        <v-card
            flat
            color="transparent"
            v-if="loading"
            class="text-center mt-10 pt-10"
        >
            <div class="lds-hourglass"></div>
        </v-card>

        <v-card tile flat color="#f8f8f8" v-else>
            <v-card-text>
                <h1
                    class="text-xs-h7 text-md-h3 pb-3 font-weight-bold primary--text"
                >
                    Coronavirus in der Städteregion Aachen
                </h1>
            </v-card-text>
            <v-card-text class="pb-0 caption"> Stand: {{ date }} </v-card-text>
            <v-card-title class="text-xs-h7 text-lg-h4 pb-0 font-weight-bold">
                Übersicht Städteregion Aachen<br />
            </v-card-title>
            <v-card-text class="py-3 px-1" v-if="!loading">
                <Indicator
                    :value="sr.today.rollingRate"
                    title="Inzidenz"
                    description="Die Inzidenz gibt an, wie viele Personen pro 100.000 Einwohner in den letzten 7 Tagen positiv auf COVID-19 getestet wurden"
                    :trend="computeTrend(sr.today.rollingRate, 50, 200)"
                />
                <Indicator
                    :value="`${Math.round(sr.today.rollingRatePerc * 100, 2)}%`"
                    title="Inzidenz-Wachstum"
                    description="Die Wachstumsrate der Inzidenz. Verglichen wird die letzte Woche mit der Vorwoche. Dies entspricht dem 7-Tage-R-Wert."
                    :trend="computeTrend(sr.today.rollingRatePerc * 100, -5, 0)"
                    middleColor="#d0d0d0"
                />
                <Indicator
                    :value="divi.today.freeBeds"
                    title="freie Betten"
                    description="Freie Intensivbetten in der Städteregion Aachen"
                    :trend="divi.today.freeBeds > 10 ? 1 : -1"
                />
                <Indicator
                    :value="quicktests.positive[0]"
                    title="positive Schnelltests"
                    :description="`Anzahl positiver Bürgerschnelltests am ${quicktests.dateFormatted}`"
                    :trend="computeTrend(quicktests.positive[0], 5, 15)"
                    :ntrend="quicktests.positive[0]>0 ? -1 : 1"
                />
            </v-card-text>
            <v-card-text class="py-0" v-if="!loading">
                <v-row>
                    <v-col cols="12" md="4">
                        <MiniChartNew
                            :start="150"
                            :date="sr.date"
                            :today="sr.today.rollingRate"
                            :weekChange="
                                Math.round(sr.trend.rollingRate7DayChange)
                            "
                            :weekChangePercent="
                                Math.round(
                                    sr.trend.rollingRate7DayChangePercent * 100
                                )
                            "
                            description="Positiv getestete Personen der letzten 7 Tage pro 100.000 Einwohner"
                            title="7-Tage-Inzidenz"
                            attribute="incidence"
                            :data="sr.rollingRate"
                        />
                    </v-col>
                    <v-col cols="12" md="4">
                        <MiniChartNew
                            :start="150"
                            :date="sr.date"
                            :today="sr.today.cumCases"
                            :weekChange="
                                Math.round(sr.trend.cumCases7DayChange)
                            "
                            :weekChangePercent="
                                Math.round(
                                    sr.trend.cumCases7DayChangePercent * 100
                                )
                            "
                            description="Positiv getestete Personen"
                            title="Fälle"
                            attribute="positive"
                            :data="sr.cumCases"
                            sum
                            :sumWeek="sr.trend.cumCases7DaySum"
                            :sum2Week="sr.trend.cumCases14DaySum"
                        />
                    </v-col>
                    <v-col cols="12" md="4">
                        <MiniChartNew
                            :start="150"
                            :date="sr.date"
                            :today="sr.today.activeCases"
                            :weekChange="
                                Math.round(sr.trend.activeCases7DayChange)
                            "
                            :weekChangePercent="
                                Math.round(
                                    sr.trend.activeCases7DayChangePercent * 100
                                )
                            "
                            description="Aktive Fälle"
                            title="Aktive Fälle"
                            attribute="active"
                            :data="sr.activeCases"
                        />
                    </v-col>
                </v-row>
            </v-card-text>
            <v-divider></v-divider>
            <v-card-title
                class="text-xs-h7 text-lg-h4 pb-0 pt-10 font-weight-bold"
            >
                Übersicht Stadt Aachen
                <v-spacer></v-spacer>
            </v-card-title>
            <v-card-text class="py-3 px-1" v-if="!loading">
                <Indicator
                    :value="aachen.today.rollingRate"
                    title="Inzidenz"
                    description="Die Inzidenz gibt an, wie viele Personen pro 100.000 Einwohner in den letzten 7 Tagen positiv auf COVID-19 getestet wurden"
                    :trend="computeTrend(aachen.today.rollingRate, 50, 200)"
                />
                <Indicator
                    :value="`${Math.round(aachen.today.rollingRatePerc * 100, 2)}%`"
                    title="Inzidenz-Wachstum"
                    description="Die Wachstumsrate der Inzidenz. Verglichen wird die letzte Woche mit der Vorwoche. Dies entspricht dem 7-Tage-R-Wert."
                    :trend="computeTrend(aachen.today.rollingRatePerc * 100, -5, 0)"
                    middleColor="#d0d0d0"
                />
            </v-card-text>

            <v-card-text class="py-0" v-if="!loading">
                <v-row>
                    <v-col cols="12" md="4">
                        <MiniChartNew
                            :date="aachen.date"
                            muni="aachen"
                            :today="aachen.today.rollingRate"
                            :weekChange="
                                Math.round(aachen.trend.rollingRate7DayChange)
                            "
                            :weekChangePercent="
                                Math.round(
                                    aachen.trend.rollingRate7DayChangePercent *
                                        100
                                )
                            "
                            description="Infektionen der letzten 7 Tage pro 100.000 Einwohner"
                            title="7-Tage-Inzidenz"
                            attribute="incidence"
                            :data="aachen.rollingRate"
                        />
                    </v-col>
                    <v-col cols="12" md="4">
                        <MiniChartNew
                            :date="aachen.date"
                            :today="aachen.today.cumCases"
                            :weekChange="
                                Math.round(aachen.trend.cumCases7DayChange)
                            "
                            :weekChangePercent="
                                Math.round(
                                    aachen.trend.cumCases7DayChangePercent * 100
                                )
                            "
                            description="Positiv getestete Personen"
                            title="Fälle"
                            attribute="positive"
                            :data="aachen.cumCases"
                            sum
                            :sumWeek="aachen.trend.cumCases7DaySum"
                            :sum2Week="aachen.trend.cumCases14DaySum"
                        />
                    </v-col>
                    <v-col cols="12" md="4">
                        <MiniChartNew
                            :date="aachen.date"
                            :today="aachen.today.activeCases"
                            :weekChange="
                                Math.round(aachen.trend.activeCases7DayChange)
                            "
                            :weekChangePercent="
                                Math.round(
                                    aachen.trend.activeCases7DayChangePercent *
                                        100
                                )
                            "
                            description="Aktive Fälle"
                            title="Aktive Fälle"
                            attribute="active"
                            :data="aachen.activeCases"
                        />
                    </v-col>
                </v-row>
            </v-card-text>
            <v-card-text v-if="!loading" class="text-right">
                Datenquelle:
                <a
                    target="_blank"
                    href="https://offenedaten.aachen.de/dataset/aktuelle-lage-zum-corona-virus"
                    >Open Data Portal der Stadt Aachen</a
                >.
            </v-card-text>
            <v-divider></v-divider>
            <v-card-text class="mt-10" v-if="!loading">
                <h3 class="text-h6 text-md-h4 black--text text-uppercase my-3">
                    Tabellarische Übersicht
                </h3>
                <div class="pb-3">
                    Klicke auf eine Kommune, um weitere Informationen zu
                    erhalten
                </div>
                <OverviewTable :data="overview"></OverviewTable>
                <v-card-text class="caption text-right">
                    Die Pfeile
                    <v-icon small color="red">fa fa-chevron-down</v-icon>
                    <v-icon small color="green">fa fa-chevron-up</v-icon> geben
                    den 7-Tage-Trend wieder.
                </v-card-text>
            </v-card-text>

            <v-card-text class="mt-10">
                <h3 class="text-h6 text-md-h4 black--text text-uppercase my-3">
                    Intensivbetten in der Städteregion Aachen
                </h3>
                <hospital-table :data="divi"></hospital-table>
            </v-card-text>
            <v-divider></v-divider>
            <v-card-text class="mb-5">
                <v-list>
                    <v-list-item>
                        <v-list-item-icon>
                            <v-icon large color="#1B9AAA"
                                >fa fa-info-circle</v-icon
                            >
                        </v-list-item-icon>
                        <v-list-item-content class="caption text-md-body-1 ">
                            Aktuelle Informationen zum Corona-Virus inklusive
                            der gerade gültigen Verordnungen der Städteregion
                            Aachen findet man unter
                            <b
                                ><a
                                    target="_blank"
                                    href="https://www.staedteregion-aachen.de/corona"
                                >
                                    www.staedteregion-aachen.de/corona</a
                                ></b
                            >
                        </v-list-item-content>
                    </v-list-item>
                </v-list>
            </v-card-text>
        </v-card>
    </v-container>
</template>

<script>
import Mini from "./charts/Mini.vue";
import MiniChartNew from "./charts/MiniChartNew.vue";

import OverviewTable from "./OverviewTable.vue";
import HospitalTable from "./HospitalTable.vue";

import Indicator from "@/components/Indicator.vue";

import { format } from "echarts";
import axios from "axios";
import _ from "lodash";

const API = process.env.VUE_APP_CORONA_API_NEW;

export default {
    name: "CoronaMain",
    data: () => ({
        sr: null,
        aachen: null,
        divi: null,
        overview: null,
        quicktests: null,
        loading: true
    }),
    methods: {
        computeTrend(v, min, max) {
            if (v < min) {
                return 1;
            }
            if (v > max) {
                return -1;
            }
            return 0;
        },
        async load() {
            await axios
                .get(`${API}/muni/sr?fields=rollingRate,activeCases,cumCases`)
                .then(response => {
                    this.sr = response.data;
                });
            await axios
                .get(
                    `${API}/muni/aachen?fields=rollingRate,activeCases,cumCases`
                )
                .then(response => {
                    this.aachen = response.data;
                });
            await axios.get(`${API}/divi/`).then(response => {
                this.divi = response.data;
            });
            await axios.get(`${API}/quicktests/?limit=1&sort=-1`).then(response => {
                this.quicktests = response.data;
            });
            await axios.get(`${API}/overview/`).then(response => {
                this.overview = response.data;
            });
            this.loading = false;
        }
    },
    async mounted() {
        this.load();
    },
    components: {
        Mini,
        MiniChartNew,
        OverviewTable,
        HospitalTable,
        Indicator
    },
    metaInfo: {
        title: "Corona-Dashboard für die Stadt und Städteregion Aachen",
        meta: [
            {
                name: "description",
                content:
                    "Alle Corona-Daten für die Städteregion Aachen: Inzidenzen, Fallzahlen, Intensivbelegung und deren Entwicklung"
            }
        ]
    },

    computed: {
        date() {
            return this.sr && format.formatTime("dd.MM.yyyy", this.sr.date);
        }
    }
};
</script>
<style scoped>
h1 {
    line-height: 1.2 !important;
}
</style>
