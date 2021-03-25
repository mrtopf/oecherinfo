<template>
    <DataView
        title="Corona-Tests"
        :loading="loading"
        hide-muni-selector
        muni="sr"
        :data="data"
        :attribute="attribute"
        :keyAttributes="keyAttributes"
        :downloadUrl="downloadUrl"
        :date="date"
    >
        <template v-slot:graphs>
            <Panel
                title="kostenlose Bürgerschnelltests"
                matomoAttribute="quicktests"
                attribute="quicktests"
                hide-header
                show-about
                :data="data"
                :tableAttributes="[
                    { value: 'total', text: 'Gesamtzahl Tests' },
                    { value: 'positive', text: 'positive Tests' },
                    { value: 'negative', text: 'negative Tests' },
                    { value: 'rate_percent', text: 'Positivrate' }
                ]"
                :tabs="[{ id: 'daily', title: 'Täglich' }]"
            >
                <template v-slot:description>
                    Anzahl der durchgeführten kostenlosen Bürgerschnelltests und der positiven Ergebnisse in der Städteregion Aachen
                </template>
                <template v-slot:tab.daily>
                    <QuickTestChart
                        :labels="data.dates"
                        :data="data"
                        name="Anzahl Schnelltests"
                    >
                    </QuickTestChart>
                </template>
                <template v-slot:tab.about>
                    <p>
                        Die Zahlen spiegeln die kostenlose Bürgerschnelltests
                        wieder, die in den
                        <a
                            href="https://www.staedteregion-aachen.de/de/navigation/aemter/oeffentlichkeitsarbeit-s-13/aktuelles/corona-schnelltest"
                            target="_blank"
                            >Testzentren</a
                        >
                        durchgeführt werden.
                    </p>

                    <p>
                        Da symptomatische Personen gebeten werden, einen
                        kostenlosen PCR-Test zu machen und keinen Bürgertest,
                        ist die Positivenquote hier immer niedriger als bei den
                        PCR-Tests.
                    </p>

                    <p>
                        Nicht erfasst werden Tests in den Schulen, Unternehmen,
                        Behörden und Krankenhäusern, da diese nicht
                        meldepflichtig sind.
                    </p>
                    <p>
                        Für die Berechnung des Inzidenzwertes zählt nur die
                        Anzahl der positiven PCR-Tests, auch diese sind hier
                        nicht erfasst. Die Gesamtzahl aller in der StädteRegion
                        durchgeführten PCR-Tests wird von den Laboren direkt an
                        das RKI übermittelt und ist der Städteregion Aachen
                        deshalb nicht bekannt.
                    </p>
                    <p>
                        Die Daten werden uns freundlicherweise von der
                        Städteregion Aachen zur Verfügung gestellt und können
                        als CSV-Datei
                        <a :href="downloadUrl" target="_blank">hier</a>
                        abgerufen werden. Unter dieser URL sind immer die aktuellen Daten zu finden. 
                        Eine JSON-Schnittstelle ist unter <a :href="downloadUrlJson" target="_blank">{{downloadUrlJson}}</a> erhältlich.
                    </p>
                </template>
            </Panel>
        </template>
    </DataView>
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";
import DataView from "@/components/DataView.vue";
import Panel from "@/components/Panel.vue";
import QuickTestChart from "@/components/charts/QuickTestChart.vue";
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
    name: "RecoveredView",
    mounted() {
        this.load();
    },
    methods: {
        load() {
            axios.get(`${API}/quicktests/`).then(response => {
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
                name: "Schnelltests",
                item: "total",
                width: 150
            },
            {
                name: "Positiv",
                item: "positive",
                width: 100
            },
            {
                name: "Positivrate",
                item: "rate_formatted",
                width: 200
            }
        ]
    }),
    metaInfo() {
        return genMetaInfo(
            `COVID-19: Anzahl Schnelltests Städteregion Aachen`,
            `Aktuelle Zahlen und Entwicklung Schnelltests Städteregion Aachen`
        );
    },

    computed: {
        downloadUrlJson() {
            return `${API}/quicktests/`;
        },
        downloadUrl() {
            return `${API}/quicktests/?format=csv`;
        },
        date() {
            return this.data && format.formatTime("dd.MM.yyyy", this.data.date);
        },
        todayData() {
            return {
                today: {
                    total: this.data["total"][0],
                    positive: this.data["positive"][0]
                }
            };
        }
    },
    components: {
        DataView,
        Panel,
        QuickTestChart
    }
};
</script>
