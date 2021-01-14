<template>
    <v-container fluid class="pa-0">
        <v-card tile flat color="#f8f8f8">
            <v-card-text>
                <h1
                    class="text-xs-h7 text-md-h3 pb-3 font-weight-bold primary--text"
                >
                    Coronavirus in der Städteregion Aachen
                </h1>
            </v-card-text>
            <v-card-text class="pb-0 caption"> Stand: {{ date }} </v-card-text>
            <v-card-title class="text-xs-h7 text-lg-h5 pb-0 font-weight-bold">
                Übersicht Städteregion Aachen
            </v-card-title>

            <v-card-text class="py-0" v-if="loaded">
                <v-row>
                    <v-col cols="12" md="4">
                        <MiniChart
                            description="Infektionen der letzten 7 Tage pro 100.000 Einwohner"
                            title="7-Tage-Inzidenz"
                            attribute="incidence"
                        />
                    </v-col>
                    <v-col cols="12" md="4">
                        <MiniChart
                            description="Positiv getestete Personen"
                            title="Fälle"
                            attribute="positive"
                            sum
                        />
                    </v-col>
                    <v-col cols="12" md="4">
                        <MiniChart
                            description="Aktuell positiv getestete Personen"
                            title="Aktive Fälle"
                            attribute="active"
                        />
                    </v-col>
                </v-row>
            </v-card-text>
            <v-card-title
                class="text-xs-h7 text-lg-h5 pb-0 pt-10 font-weight-bold"
            >
                Übersicht Stadt Aachen
                <v-spacer></v-spacer>
            </v-card-title>

            <v-card-text class="py-0" v-if="loaded">
                <v-row>
                    <v-col cols="12" md="4">
                        <MiniChart
                            description="Infektionen der letzten 7 Tage pro 100.000 Einwohner"
                            title="7-Tage-Inzidenz"
                            attribute="incidence"
                            muni="aachen"
                        />
                    </v-col>
                    <v-col cols="12" md="4">
                        <MiniChart
                            description="Positiv getestete Personen"
                            title="Fälle"
                            attribute="positive"
                            muni="aachen"
                            sum
                        />
                    </v-col>
                    <v-col cols="12" md="4">
                        <MiniChart
                            description="Aktuell positiv getestete Personen"
                            title="Aktive Fälle"
                            attribute="active"
                            muni="aachen"
                        />
                    </v-col>
                </v-row>
            </v-card-text>
            <v-card-text v-if="loaded" class="text-right">
                Datenquelle:
                <a
                    target="_blank"
                    href="https://offenedaten.aachen.de/dataset/aktuelle-lage-zum-corona-virus"
                    >Open Data Portal der Stadt Aachen</a
                >.
            </v-card-text>
            <v-card-text class="mt-10" v-if="loaded">
                <h3 class="text-h6 text-md-h4 black--text text-uppercase my-3">
                    Tabellarische Übersicht
                </h3>
                <div class="pb-3">
                    Klicke auf eine Kommune, um weitere Informationen zu
                    erhalten
                </div>
                <OverviewTable></OverviewTable>
            </v-card-text>

            <v-card-text class="mt-10">
                <h3 class="text-h6 text-md-h4 black--text text-uppercase my-3">
                    Intensivbetten in der Städteregion Aachen
                </h3>
                <hospital-table></hospital-table>
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
import Incidence from "./charts/Incidence.vue";
import NewCases from "./charts/NewCases.vue";
import MiniNew from "./charts/MiniNew.vue";
import MiniChart from "./charts/MiniChart.vue";

import OverviewTable from "./OverviewTable.vue";
import HospitalTable from "./HospitalTable.vue";

import { mapState, mapActions, mapGetters } from "vuex";

import axios from "axios";

import _ from "lodash";

const API = process.env.VUE_APP_CORONA_API;

export default {
    name: "CoronaMain",
    data: () => ({
        range: [0, 100],
        startSelected: "w2",
        // diff sr to rest: 180-54
        startDict: {
            all: "Gesamtzeitraum",
            w2: "2. Welle",
            "14tage": "14 Tage"
        },
        secondWave: true
    }),
    methods: {
        ...mapActions({
            updateMuni: "corona/updateMuni",
            load: "corona/load"
        })
    },
    async mounted() {},
    components: {
        Mini,
        MiniNew,
        MiniChart,
        Incidence,
        NewCases,
        OverviewTable,
        HospitalTable
    },
    computed: {
        startIndex() {
            if (this.startSelected == "w2") {
                return this.selectedMuni == "sr" ? 180 : 54;
            } else if (this.startSelected == "14tage") {
                const l = this.muni_data["incidence"].length;
                return l - 14;
            } else {
                return 1;
            }
        },
        ...mapGetters("corona", ["muniName", "muni_data", "todayList"]),
        ...mapState({
            muniDict: state => state.corona.muniDict,
            loaded: state => state.corona.loaded,
            munis: state => state.corona.munis,
            divi: state => state.corona.divi,
            today: state => state.corona.today,
            yesterday: state => state.corona.yesterday,
            weekerday: state => state.corona.weekerday,
            date: state => state.corona.date,
            yesterdate: state => state.corona.yesterdate,
            selectedMuni: state => state.corona.selectedMuni
        })
    }
};
</script>
<style scoped>
h1 {
    line-height: 1.2 !important;
}
</style>
