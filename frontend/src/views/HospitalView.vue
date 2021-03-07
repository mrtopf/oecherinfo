<template>
    <v-card color="transparent" flat>
        <DataView
            title="Krankenhaussituation Städteregion Aachen"
            :loading="loading"
            :data="data"
            hide-muni-selector
            :keyAttributes="keyAttributes"
            :attribute="attribute"
            :date="date"
        >
            <template v-slot:graphs>
                <Panel
                    title="freie Betten"
                    :showTrends="false"
                    matomoAttribute="beds"
                    attribute="freeBeds"
                    :data="data"
                    :tableAttributes="[
                        { value: 'allBeds', text: 'alle Betten' },
                        { value: 'occupiedBeds', text: 'belegte Betten' },
                        {
                            value: 'avgAllBeds',
                            text: 'Durchschnitt, alle Betten'
                        },
                        {
                            value: 'avgOccupiedBeds',
                            text: 'Durchschnitt, belegte Betten'
                        }
                    ]"
                    :tabs="[{ id: 'daily', title: 'täglich' }]"
                >
                    <template v-slot:description>
                        <summary>
                            Anzahl der Betten auf den Intensivstationen der
                            Städteregion Aachen
                        </summary>
                    </template>
                    <template v-slot:tab.daily>
                        <BedChart
                            :labels="data.dates"
                            :data="data"
                            name="Betten"
                        >
                        </BedChart>
                    </template>
                </Panel>

                <Panel
                    title="COVID-19-Fälle"
                    matomoAttribute="covid"
                    attribute="covid19Cases"
                    :data="data"
                    :tableAttributes="[
                        { value: 'covid19Cases', text: 'freie Betten' },
                        {
                            value: 'avgCovid19Cases',
                            text: 'Durchschnitt der letzten 7 Tage'
                        }
                    ]"
                    :tabs="[{ id: 'daily', title: 'Täglich' }]"
                >
                    <template v-slot:description>
                        <summary>
                            Anzahl der Betten auf Intensivstationen, die mit
                            COVID-19-Patienten belegt sind.
                        </summary>
                    </template>
                    <template v-slot:tab.daily>
                        <Chart
                            :labels="data.dates"
                            :data="data.covid19Cases"
                            :avgs="data.avgCovid19Cases"
                            name="COVID-19-Fälle"
                        >
                        </Chart>
                    </template>
                </Panel>

                <Panel
                    title="COVID-19-Fälle, beatmet"
                    matomoAttribute="ventilated"
                    attribute="ventilatorCases"
                    :data="data"
                    :tableAttributes="[
                        { value: 'ventilatorCases', text: 'COVID-19, beatmet' },
                        {
                            value: 'avgVentilatorCases',
                            text: 'Durchschnitt der letzten 7 Tage'
                        }
                    ]"
                    :tabs="[{ id: 'daily', title: 'Täglich' }]"
                >
                    <template v-slot:description>
                        <summary>
                            Anzahl der Betten auf Intensivstationen, die mit
                            COVID-19-Patienten belegt sind, die beatmet werden
                            müssen.
                        </summary>
                    </template>
                    <template v-slot:tab.daily>
                        <Chart
                            :labels="data.dates"
                            :data="data.ventilatorCases"
                            :avgs="data.avgVentilatorCases"
                            name="COVID-19-Fälle, beatmet"
                        >
                        </Chart>
                    </template>
                </Panel>
            </template>
        </DataView>
        <v-card-text class="mb-5">
            <v-list>
                <v-list-item>
                    <v-list-item-icon>
                        <v-icon color="#1B9AAA">fa fa-info-circle</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content class="caption ">
                        Diese Daten werden vom
                        <a
                            target="_blank"
                            href="https://www.intensivregister.de/#/index"
                        >
                            DIVI-Intensivregister</a
                        >
                        bereitgestellt. Dort findet man auch weitere Daten,
                        Zeitreihen und Downloads.
                    </v-list-item-content>
                </v-list-item>
            </v-list>
        </v-card-text>
    </v-card>
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";
import DataView from "@/components/DataView.vue";
import Panel from "@/components/Panel.vue";
import Chart from "@/components/Chart.vue";
import BedChart from "@/components/charts/BedChart.vue";
import { format } from "echarts";
import { genMetaInfo } from "@/utils.js";

const API = process.env.VUE_APP_CORONA_API_NEW;

export default {
    props: {
        attribute: String
    },
    name: "HospitalView",
    mounted() {
        this.load();
    },
    methods: {
        load() {
            axios.get(`${API}/divi/`).then(response => {
                this.data = response.data;
                this.loading = false;
            });
        }
    },
    watch: {
        muni(v) {
            this.load();
        }
    },

    data: () => ({
        loading: true,
        data: null,
        keyAttributes: [
            {
                name: "Gesamtzahl",
                item: "allBeds",
                width: 150
            },
            {
                name: "belegt",
                item: "occupiedBeds",
                width: 150
            },
            {
                name: "frei",
                item: "freeBeds",
                width: 150
            },
            {
                name: "COVID-19-Fälle",
                item: "covid19Cases",
                width: 150
            },
            {
                name: "davon beatmet",
                item: "ventilatorCases",
                width: 150
            }
        ]
    }),
    metaInfo() {
        return genMetaInfo(
            "COVID-19: Intensivbettenbelegung Städteregion Aachen",
            "Aktuelle Lage der Intensivbettenbelegung der Krankenhäuser in der Städteregion Aachen"
        );
    },

    computed: {
        date() {
            return this.data && format.formatTime("dd.MM.yyyy", this.data.date);
        }
    },
    components: {
        DataView,
        Panel,
        Chart,
        BedChart
    }
};
</script>
