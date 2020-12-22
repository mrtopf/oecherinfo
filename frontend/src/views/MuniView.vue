<template>
    <v-container
        fluid
        class="d-flex child-flex flex-column pa-0"
        style="nbackground: green"
    >
        <v-card class="ma-0 flex-grow-1 flex-shrink-0" ref="tabCard">
            <v-toolbar color="white" flat>
                <v-toolbar-title class="font-weight-bold text-uppercase"
                    >{{ muniDict[muni] }}
                    <v-menu offset-y bottom left>
                        <template v-slot:activator="{ on }">
                            <v-btn color="primary" dark icon v-on="on">
                                <v-icon>fa fa-caret-down</v-icon>
                            </v-btn>
                        </template>
                        <v-list dense nav>
                            <v-list-item
                                v-for="item in $store.state.corona.munis"
                                :key="item.value"
                                link
                                :to="{
                                    name: 'munidata',
                                    params: {
                                        attribute: 'incidence',
                                        muni: item.muni,
                                    },
                                }"
                            >
                                <v-list-item-content>
                                    <v-list-item-title>{{
                                        item.name
                                    }}</v-list-item-title>
                                </v-list-item-content>
                            </v-list-item>
                        </v-list>
                    </v-menu>
                </v-toolbar-title>
                <v-spacer></v-spacer>
                <v-menu offset-y bottom left>
                    <template v-slot:activator="{ on }">
                        <v-btn
                            color="oecheryellow darken-1"
                            dark
                            icon
                            v-on="on"
                        >
                            <v-icon>fa fa-calendar-alt</v-icon>
                        </v-btn>
                    </template>
                    <v-list>
                        <v-list-item class="font-weight-bold text-uppercase">
                            <v-icon small left>fa fa-calendar-alt</v-icon>

                            Zeitfenster
                        </v-list-item>
                        <v-divider></v-divider>
                        <v-list-item @click="setStart('all')"
                            >komplett</v-list-item
                        >
                        <v-list-item @click="setStart('w2')"
                            >2. Welle</v-list-item
                        >
                        <v-list-item @click="setStart('14tage')"
                            >14 Tage</v-list-item
                        >
                    </v-list>
                </v-menu>
            </v-toolbar>
            <v-tabs
                centered
                v-model="activeTab"
                background-color="primary"
                dark
            >
                <v-tab exact v-for="tab in Object.keys(tabs)" :key="tab">
                    {{ tabs[tab] }}
                </v-tab>
            </v-tabs>
            <v-card-text>
                <div class="legend">
                    Stand {{ date }}<br />
                    <span class="l1-line"></span> Lockdown Light, 2.11.2020<br />
                    <span class="l2-line"></span> Weihnachts-Lockdown,
                    16.12.2020
                </div>
            </v-card-text>

            <v-tabs-items v-model="activeTab" ref="tabs">
                <v-tab-item v-for="tab in Object.keys(tabs)" :key="tab">
                    <CoronaGraph
                        :chartHeight="chartHeight"
                        :chartWidth="chartWidth"
                        :dateRange="dateRange"
                        :attribute="tab"
                        :muni="muni"
                    />
                </v-tab-item>
            </v-tabs-items>
        </v-card>
    </v-container>
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";

import CoronaGraph from "@/components/CoronaGraph.vue";

export default {
    props: {
        muni: String,
        attribute: String,
    },
    name: "MuniView",
    data: () => ({
        activeTab: "incidence",
        chartHeight: 500,
        chartWidth: 500,
        startMenu: false,
        startDate: new Date("2020-09-17").toISOString().substr(0, 7),
        endMenu: false,
        endDate: new Date().toISOString().substr(0, 7),
        dateRange: [180, 190],
        myChart: null,
        chartTypes: {
            incidence: "line",
            new: "bar",
            active: "line",
            positive: "line",
            recovered: "line",
            deaths: "line",
        },
        tabs: {
            incidence: "Inzidenz",
            new: "neu",
            active: "aktiv",
            positive: "Fälle",
            recovered: "Genesen",
            deaths: "Tote",
        },
        titles: {
            incidence: "7-Tage-Inzidenz",
            new: "Neue Fälle",
            active: "Aktive Fälle",
            positive: "Fälle insgesamt",
            recovered: "Genesen insgesamt",
            deaths: "Todesfälle insgesamt",
        },
    }),
    mounted() {
        if (this.muni_data) {
            this.dateRange = [0, this.muni_data.incidence.length];
        }
    },
    watch: {
        muni_data(val, oldval) {
            this.dateRange = [0, val.incidence.length];
        },
    },
    methods: {
        setStart(startSelected) {
            const end = this.muni_data.incidence.length;
            if (startSelected == "w2") {
                this.dateRange = [this.muni == "sr" ? 180 : 54, end];
            } else if (startSelected == "14tage") {
                this.dateRange = [end - 15, end];
            } else if (startSelected == "all") {
                this.dateRange = [0, end];
            } else {
                this.dateRange = [0, end];
            }
        },

        saveStartDate(date) {
            this.startDate = new Date(date);
        },
        saveEndDate(date) {
            this.endDate = new Date(date);
        },
        createChart(chartId, chartData) {
            const ctx = document.getElementById("incidence-chart");
            this.myChart = new Chart(ctx, {
                type: chartData.type,
                data: chartData.data,
                options: chartData.options,
            });
        },

        ...mapActions({
            updateMuni: "corona/updateMuni",
        }),
    },
    components: {
        CoronaGraph,
    },
    computed: {
        muni_data() {
            return this.allMuniData[this.muni];
        },
        ...mapGetters("corona", ["muniName"]),
        ...mapState({
            muniDict: (state) => state.corona.muniDict,
            loaded: (state) => state.corona.loaded,
            munis: (state) => state.corona.munis,
            allMuniData: (state) => state.corona.allMuniData,
            today: (state) => state.corona.today,
            date: (state) => state.corona.date,
        }),
    },
};
</script>
<style lang="scss">
.l1-line {
    display: inline-block;
    border-top: 3px dashed #f78656;
    padding-top: 2px;
    width: 40px;
}
.l2-line {
    display: inline-block;
    border-top: 3px dashed #ef476f;
    padding-top: 2px;
    width: 40px;
}
.legend {
    text-align: right;
    font-size: 0.7rem;
    color: black;
}
</style>
