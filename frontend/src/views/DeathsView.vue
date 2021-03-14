<template>
    <DataView
        title="Todesfälle"
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
                title="Todesfälle"
                matomoAttribute="recovered"
                attribute="recoveredCases"
                :data="data"
                :tableAttributes="[
                    { value: 'newDeaths', text: 'Todesfälle' },
                    {
                        value: 'avgNewDeaths',
                        text: 'Durchschnitt der letzten 7 Tage'
                    },
                    { value: 'cumDeaths', text: 'kumulierte Fälle' }
                ]"
                :tabs="[
                    { id: 'daily', title: 'Täglich' },
                    { id: 'cum', title: 'Kumuliert' }
                ]"
            >
                <template v-slot:description>
                    <summary>
                        Die Anzahl der Personen, die an oder mit COVID-19
                        verstorben sind.
                    </summary>
                </template>
                <template v-slot:tab.daily>
                    <Chart
                        :labels="data.dates"
                        :data="data.newDeaths"
                        :avgs="data.avgNewDeaths"
                        name="Todesfälle"
                    >
                    </Chart>
                </template>
                <template v-slot:tab.cum>
                    <Chart
                        :labels="data.dates"
                        :data="data.cumDeaths"
                        name="kumuliert"
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
import Chart from "@/components/charts/Chart.vue";
import { format } from "echarts";
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
    name: "DeathsView",
    mounted() {
        this.load();
    },
    methods: {
        load() {
            axios
                .get(
                    `${API}/muni/${this.muni}?fields=newDeaths,cumDeaths,avgNewDeaths`
                )
                .then(response => {
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
                name: "heute",
                item: "newDeaths",
                width: 150
            },
            {
                name: "Insgesamt",
                item: "cumDeaths",
                width: 200
            }
        ]
    }),
    metaInfo() {
        return genMetaInfo(
            `COVID-19: Todesfälle für ${MUNI_DICT[this.muni]}`,
            `Aktuelle Daten zur Entwicklung der Todesfälle für ${
                MUNI_DICT[this.muni]
            }.`
        );
    },

    computed: {
        downloadUrl() {
            return `${API}/muni/${this.muni}?format=csv`;
        },
        date() {
            return this.data && format.formatTime("dd.MM.yyyy", this.data.date);
        }
    },
    components: {
        DataView,
        Panel,
        Chart
    }
};
</script>
