<template>
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
                        Anzahl der Betten auf Intensivstationen
                    </summary>
                </template>
                <template v-slot:tab.daily>
                    <BedChart :labels="data.dates" :data="data" name="Betten">
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
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";
import DataView from "@/components/DataView.vue";
import Panel from "@/components/Panel.vue";
import Chart from "@/components/Chart.vue";
import BedChart from "@/components/charts/BedChart.vue";
import { format } from "echarts";

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
