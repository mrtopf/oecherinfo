<template>
    <div>
        <DataView
            title="Fallzahlen"
            :loading="loading"
            :muni="muni"
            :data="data"
            :keyAttributes="keyAttributes"
            :attribute="attribute"
            :downloadUrl="downloadUrl"
            :date="date"
        >
            <template v-slot:graphs>
                <Panel
                    title="7-Tage-Inzidenz"
                    matomoAttribute="incidence"
                    attribute="rollingRate"
                    :data="data"
                    :tableAttributes="[
                        { value: 'rollingRate', text: '7-Tage-Inzidenz' },
                        {
                            value: 'avgRollingRate',
                            text: 'Durchschnitt der letzten 7 Tage'
                        },
                        {
                            value: 'rollingRatePerc',
                            text: 'Prozentuale Änderung'
                        }
                    ]"
                    :tabs="[
                        { id: 'daily', title: 'Täglich' },
                        { id: 'percent', title: 'Änderung in Prozent' }
                    ]"
                >
                    <template v-slot:description>
                            Die Sieben-Tage-Inzidenz gibt an, wie viele Personen
                            in den letzten 7 Tagen positiv auf COVID-19 getestet
                            wurden. Damit die Daten vergleichbar sind, wird die
                            Zahl der Neuinfektionen je 100.000 Einwohner
                            berechnet. Die prozentuale Änderung wird anhand des
                            vorherigen 7-Tage-Zeitraums berechnet.
                    </template>
                    <template v-slot:tab.daily>
                        <Chart
                            :labels="data.dates"
                            :data="data.rollingRate"
                            :avgs="data.avgRollingRate"
                            name="7-Tage-Inzidenz"
                            showLines
                            showVisualMap="rollingRate"
                        >
                        </Chart>
                    </template>
                    <template v-slot:tab.percent>
                        <Chart
                            :labels="data.dates"
                            :data="data.rollingRatePerc"
                            name="Prozentuale Änderung"
                            startZoom="2020-12-15"
                        >
                        </Chart>
                    </template>
                </Panel>

                <Panel
                    title="Neue Fälle"
                    matomoAttribute="cases"
                    attribute="newCases"
                    :data="data"
                    :tableAttributes="[
                        { value: 'newCases', text: 'Neue Fälle' },
                        {
                            value: 'avgNewCases',
                            text: 'Durchschnitt der letzten 7 Tage'
                        },
                        { value: 'cumCases', text: 'kumulierte Fälle' }
                    ]"
                    :tabs="[
                        { id: 'daily', title: 'Täglich' },
                        { id: 'cum', title: 'Kumuliert' }
                    ]"
                >
                    <template v-slot:description>
                            Die Anzahl der neu an COVID-19 positiv getesteten
                            Personen pro Tag.
                    </template>
                    <template v-slot:tab.daily>
                        <Chart
                            :labels="data.dates"
                            :data="data.newCases"
                            :avgs="data.avgNewCases"
                            name="Neue Fälle"
                        >
                        </Chart>
                    </template>
                    <template v-slot:tab.cum>
                        <Chart
                            :labels="data.dates"
                            :data="data.cumCases"
                            name="kumuliert"
                        >
                        </Chart>
                    </template>
                </Panel>


                <Panel
                    title="4-Tage-R-Wert"
                    matomoAttribute="rvalue"
                    attribute="r4"
                    :showTrends="false"
                    :data="data"
                    :tableAttributes="[
                        { value: 'r4', text: 'R-Wert 4 Tage' },
                        { value: 'r7', text: 'R-Wert 7 Tage' }
                    ]"
                    :tabs="[
                        { id: 'r4', title: 'R-Wert 4 Tage' },
                        { id: 'r7', title: 'R-Wert 7 Tage' }
                    ]"
                >
                    <template v-slot:trends>
                        <span class="pl-3">
                        <small>(7-Tage: {{data.today['r7'].toLocaleString("de-DE")}})</small>
                        </span>
                    </template>

                    <template v-slot:description>
                            Die Reproduktionszahl, auch R-Wert oder R-Zahl
                            genannt, gibt an, wie viele Menschen eine infizierte
                            Person in einer bestimmten Zeiteinheit im Mittel
                            ansteckt. Liegt der Wert über 1, dann steigt die
                            Zahl der Neuinfektionen, die Krankheit breitet sich
                            also weiter aus. Ist sie kleiner als 1, gibt es
                            immer weniger Neuinfektionen, die Epidemie läuft
                            also aus.</summary
                        >
                    </template>
                    <template v-slot:tab.r4>
                        <Chart
                            :labels="data.dates"
                            :data="data.r4"
                            showVisualMap="r"
                            name="R-Wert 4 Tage"
                        >
                        </Chart>
                    </template>
                    <template v-slot:tab.r7>
                        <Chart
                            :labels="data.dates"
                            :data="data.r7"
                            showVisualMap="r"
                            name="R-Wert 7 Tage"
                        >
                        </Chart>
                    </template>
                </Panel>

                <Panel
                    title="Aktive Fälle"
                    matomoAttribute="cases"
                    attribute="activeCases"
                    :data="data"
                    :tableAttributes="[
                        { value: 'activeCases', text: 'Aktive Fälle' },
                        {
                            value: 'avgActiveCases',
                            text: 'Durchschnitt der letzten 7 Tage'
                        }
                    ]"
                    :tabs="[{ id: 'daily', title: 'Täglich' }]"
                >
                    <template v-slot:description>
                            Die Anzahl der aktuell als infiziert geltenden Personen.
                    </template>
                    <template v-slot:tab.daily>
                        <Chart
                            :labels="data.dates"
                            :data="data.activeCases"
                            :avgs="data.avgActiveCases"
                            name="Aktive Fälle"
                        >
                        </Chart>
                    </template>
                </Panel>
            </template>
        </DataView>
    </div>
</template>

<script>
import axios from "axios";
import { mapState, mapActions, mapGetters } from "vuex";
import DataView from "@/components/DataView.vue";
import Panel from "@/components/Panel.vue";
import Chart from "@/components/charts/Chart.vue";
import HeatMap from "@/components/charts/HeatMap.vue";
import { format, innerDrawElementOnCanvas } from "echarts";
import { genMetaInfo, MUNI_DICT } from "@/utils.js";

const API = process.env.VUE_APP_CORONA_API_NEW;

export default {
    props: {
        muni: {
            type: String,
            default: "sr"
        },
        attribute: String
    },
    mounted() {
        this.load();
    },
    name: "CasesView",
    methods: {
        load() {
            axios
                .get(
                    `${API}/muni/${this.muni}?fields=cumCases,activeCases,avgActiveCases,newCases,avgNewCases,r4,r7,rollingRate,rollingRatePerc,avgRollingRate`
                )
                .then(response => {
                    this.data = response.data;
                    this.loading = false;
                });
            axios.get(`${API}/age/`).then(response => {
                this.age_data = response.data;
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
        age_data: null,
        keyAttributes: [
            {
                name: "Inzidenz",
                item: "rollingRate",
                width: 100
            },
            {
                name: "14-Tage-Wachstum",
                item: "rollingRatePerc100",
                width: 200,
                suffix: "%"
            },
            {
                name: "Neue Fälle",
                item: "newCases",
                width: 150
            },
            {
                name: "Aktive Fälle",
                item: "activeCases",
                width: 150
            },
            {
                name: "Gesamzahl",
                item: "cumCases",
                width: 200
            }
        ]
    }),

    computed: {
        downloadUrl() {
            return `${API}/muni/${this.muni}?format=csv`;
        },
        date() {
            return this.data && format.formatTime("dd.MM.yyyy", this.data.date);
        },
        ageData() {
            // convert weeks: [], groups: {} to [week, age, value] and [week]
            const weeks = this.age_data.weeks;
            let data = [];
            let i = 0;
            for (const group_key in this.age_data.groups) {
                const gdata = this.age_data.groups[group_key];
                for (const w in weeks) {
                    data.push([weeks[w], group_key, gdata[w]]);
                }
                i = i + 1;
            }
            return data;
        }
    },
    metaInfo() {
        return genMetaInfo(
            `COVID-19: Fallzahlen für ${MUNI_DICT[this.muni]}`,
            `Aktuelle Daten und Entwicklung der Inzidenz, neuen und aktiven Fällen sowie des R-Werts für ${
                MUNI_DICT[this.muni]
            }.`
        );
    },

    components: {
        DataView,
        Panel,
        Chart,
        HeatMap
    }
};
</script>
