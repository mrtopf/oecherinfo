<template>
    <div>
        <DataView
            title="Fallzahlen"
            :loading = "loading"
            :muni="muni"
            :data="data"
            :keyAttributes="keyAttributes"
            :attribute="attribute"
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
                        { id: 'percent', title: 'proz. Änderung' }
                    ]"
                >
                    <template v-slot:description>
                        <summary>
                            Anzahl der Personen mit durchschnittlich pro Tag
                            positiv auf COVID-19 getestenen Personen pro 100.000
                            Einwohner in den letzten 7 Tagen. Die prozentualen
                            Änderungen errechnen sich durch den Vergleich des
                            letzten 7-Tage-Zeitraums mit dem davor.
                        </summary>

                        <!-- Rate of people with at least one positive COVID-19 test
                    result (either lab-reported or lateral flow device) per
                    100,000 population in the rolling 7-day period ending on the
                    dates shown. Rates and percentage changes are presented for
                    the most recent 3 months, in order to provide transparency
                    around decision making. Percentage changes are calculated by
                    comparing to the previous non-overlapping 7-day period. -->
                    </template>
                    <template v-slot:tab.daily>
                        <Chart
                            :labels="data.dates"
                            :data="data.rollingRate"
                            :avgs="data.avgRollingRate"
                            name="7-Tage-Inzidenz"
                            showLines
                            showVisualMap
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
                        <summary>
                            Die Anzahl der neu an COVID-19 positiv getesteten
                            Personen pro Tag.
                        </summary>
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
                    title="R-Wert"
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
                    <template v-slot:description>
                        <summary>
                            Die Reproduktionszahl R besagt, wie viele weitere Personen eine einzelne Person mit COVID-19 infiziert.
                            Dies wird sowohl über einen 4-Tages- als auch einen 7-Tages-Zeitraum berechnet.
                        </summary>
                    </template>
                    <template v-slot:tab.r4>
                        <Chart
                            :labels="data.dates"
                            :data="data.r4"
                            name="R-Wert 4 Tage"
                        >
                        </Chart>
                    </template>
                    <template v-slot:tab.r7>
                        <Chart
                            :labels="data.dates"
                            :data="data.r7"
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
                        <summary>
                            Die Anzahl der aktuell an COVID-19 erkrankten
                            Personen.
                        </summary>
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
import Chart from "@/components/Chart.vue";
import { format } from "echarts";

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
        }
    },
    watch: {
        muni(v) {
            this.load()
        }
    },
    data: () => ({
        loading: true,
        data: null,
        keyAttributes: [
            {
                name: "Inzidenz",
                item: "rollingRate",
                width: 100
            },
            {
                name: "Aktive Fälle",
                item: "activeCases",
                width: 150
            },
            {
                name: "Neue Fälle",
                item: "newCases",
                width: 150
            },
            {
                name: "Gesamzahl",
                item: "cumCases",
                width: 200
            },
            {
                name: "R-Wert",
                item: "r4",
                width: 150
            }
        ]
    }),

    computed: {
        date() {
            return this.data && format.formatTime('dd.MM.yyyy', this.data.date)
        }
    },

    components: {
        DataView,
        Panel,
        Chart
    }
};
</script>
