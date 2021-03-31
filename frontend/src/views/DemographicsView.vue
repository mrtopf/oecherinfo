<template>
    <div>
        <DataView
            title="Demographische Entwicklung in der Städteregion Aachen"
            hide-muni-selector
            :loading="loading"
            muni="sr"
            :data="data"
            :attribute="attribute"
            :date="date"
        >
            <template v-slot:graphs>
                <Panel
                    v-if="data"
                    title="Inzidenz nach Altersgruppen"
                    matomoAttribute="ageIncidence"
                    attribute="ageIncidence"
                    hide-table
                    hide-header
                    :tabs="[{ id: 'heatmap', title: 'Altersverteilung' }]"
                >
                    <template v-slot:description>
                        Anzahl der mindestens einmal positiv getesteten Personen pro 100.000 Einwohner in der Städteregion Aachen, aufgeteilt nach Zeit und Altergruppe.
                    </template>
                    <template v-slot:footer>
                        <p>
                            Durch das Überfahren der Legende rechts kannst Du die entsprechenden Inzidenzen hervorheben. Weiterhin kannst Du die Ränder der Legende verschieben.
                        </p>
                        Datenquelle: Robert Koch-Institut: SurvStat@RKI 2.0,
                        <a href="https://survstat.rki.de"
                            >https://survstat.rki.de</a
                        >, Abfragedatum:
                        {{ data.incidence.updated | dateformat }}
                    </template>
                    <template v-slot:tab.heatmap>
                        <HeatMap
                            :labels="data.weeks"
                            :data="incidenceData"
                            name="Altersgruppen"
                        >
                        </HeatMap>
                    </template>
                </Panel>
                <v-row no-gutters>
                    <v-col cols=12 lg=6>
                        <Panel
                            v-if="data"
                            title="Fälle nach Alter und Geschlecht"
                            matomoAttribute="ageIncidence"
                            attribute="ageIncidence"
                            hide-table
                            hide-header
                            :tabs="[{ id: 'heatmap', title: 'Fallzahlen' }]"
                        >
                            <template v-slot:description>
                                Anzahl der Personen mit mindestens einem
                                positiven COVID-19-Test seit dem Start der
                                Pandemie. Aufgeteilt nach Alter und Geschlecht.
                            </template>
                            <template v-slot:footer>
                                Datenquelle: Robert Koch-Institut: SurvStat@RKI
                                2.0,
                                <a href="https://survstat.rki.de"
                                    >https://survstat.rki.de</a
                                >, Abfragedatum:
                                {{ data.incidence.updated | dateformat }}
                            </template>
                            <template v-slot:tab.heatmap>
                                <DoubleBarChart
                                    :labels="data.age_sex.labels"
                                    :data="[
                                        {
                                            name: 'Männlich',
                                            data: data.age_sex.male,
                                            color: '#11D0B6'
                                        },
                                        {
                                            name: 'Weiblich',
                                            data: data.age_sex.female,
                                            color: '#136F7C'
                                        }
                                    ]"
                                >
                                </DoubleBarChart>
                            </template>
                        </Panel>
                    </v-col>
                    <v-col cols=12 lg=6>
                        <Panel
                            v-if="data"
                            title="Inzidenz nach Alter und Geschlecht"
                            matomoAttribute="ageIncidence"
                            :data="data.age_sex"
                            attribute="ageIncidence"
                            hide-table
                            hide-header
                            :tabs="[{ id: 'heatmap', title: 'Inzidenz' }]"
                        >
                            <template v-slot:description>
                                Anzahl der Personen
                                <strong>pro 100.000 Einwohner</strong> mit
                                mindestens einem positiven COVID-19-Test seit
                                dem Start der Pandemie. Aufgeteilt nach Alter
                                und Geschlecht.
                            </template>
                            <template v-slot:footer>
                                Datenquelle: Robert Koch-Institut: SurvStat@RKI
                                2.0,
                                <a href="https://survstat.rki.de"
                                    >https://survstat.rki.de</a
                                >, Abfragedatum:
                                {{ data.incidence.updated | dateformat }}
                            </template>
                            <template v-slot:tab.heatmap>
                                <DoubleBarChart
                                    :labels="data.age_sex.labels"
                                    :data="[
                                        {
                                            name: 'Männlich',
                                            data: data.age_sex.male_rate,
                                            color: '#11D0B6'
                                        },
                                        {
                                            name: 'Weiblich',
                                            data: data.age_sex.female_rate,
                                            color: '#136F7C'
                                        }
                                    ]"
                                >
                                </DoubleBarChart>
                            </template>
                        </Panel>
                    </v-col>
                </v-row>
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
import DoubleBarChart from "@/components/charts/DoubleBarChart.vue";
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
            axios.get(`${API}/age/`).then(response => {
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
        data: null
    }),

    computed: {
        date() {
            return (
                this.data &&
                this.data.incidence &&
                format.formatTime("dd.MM.yyyy", this.data.incidence.updated)
            );
        },
        incidenceData() {
            console.log(this.data);
            // convert weeks: [], groups: {} to [week, age, value] and [week]
            const data = this.data.incidence;
            const weeks = data.weeks;
            let result = [];
            let i = 0;
            weeks.pop()
            for (const group_key in data.groups) {
                const gdata = data.groups[group_key];
                for (const w in weeks) {
                    result.push([weeks[w], group_key, gdata[w]]);
                }
                i = i + 1;
            }
            return result;
        }
    },
    metaInfo() {
        return genMetaInfo(
            "COVID-19: Demographische Entwicklung für die Städteregion Aachen ",
            "Altersverteilung von Inzidenz und Aufteilung nach Geschlecht-Werts"
        );
    },

    components: {
        DataView,
        Panel,
        Chart,
        HeatMap,
        DoubleBarChart
    }
};
</script>
