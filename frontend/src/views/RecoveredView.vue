<template>
    <DataView
        title="Genesene"
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
                title="Genesene"
                matomoAttribute="recovered"
                attribute="recoveredCases"
                :data="data"
                :tableAttributes="[
                    { value: 'newRecovered', text: 'Genesene' },
                    {
                        value: 'avgNewRecovered',
                        text: 'Durchschnitt der letzten 7 Tage'
                    },
                    { value: 'cumRecovered', text: 'kumulierte Fälle' }
                ]"
                :tabs="[
                    { id: 'daily', title: 'Täglich' },
                    { id: 'cum', title: 'Kumuliert' }
                ]"
            >
                <template v-slot:description>
                    <summary>
                        Die Anzahl der Personen, die an COVID-19 genesen sind.
                    </summary>
                </template>
                <template v-slot:tab.daily>
                    <Chart
                        :labels="data.dates"
                        :data="data.newRecovered"
                        :avgs="data.avgNewRecovered"
                        name="Genesene"
                    >
                    </Chart>
                </template>
                <template v-slot:tab.cum>
                    <Chart
                        :labels="data.dates"
                        :data="data.cumRecovered"
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
    name: "RecoveredView",
    mounted() {
        this.load();
    },
    methods: {
        load() {
            axios
                .get(
                    `${API}/muni/${this.muni}?fields=newRecovered,cumRecovered,avgNewRecovered`
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
                item: "newRecovered",
                width: 150
            },
            {
                name: "Insgesamt",
                item: "cumRecovered",
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
        }
    },
    components: {
        DataView,
        Panel,
        Chart
    }
};
</script>
