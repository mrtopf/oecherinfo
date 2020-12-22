<template>
    <v-container fluid fill-height style="background: green;">
        <v-row class="text-center ma-lg-1">
            <v-col cols="2">
                <Mini
                    :color="attribute == 'incidence' ? '#1B9AAA' : '#e0e0e0'"
                    :dark="attribute == 'incidence'"
                    title="7-Tage-Inzidenz"
                    no-details
                    :start="0"
                    prop="incidence"
                    :data="muni_data"
                    @click="
                        $router.push({
                            name: 'munidata',
                            params: {
                                attribute: 'incidence',
                                muni: muni,
                            },
                        })
                    "
                />
            </v-col>
            <v-col cols="2">
                <Mini
                    :color="attribute == 'new' ? '#1B9AAA' : '#e0e0e0'"
                    :dark="attribute == 'new'"
                    title="Neue Fälle"
                    no-details
                    :start="0"
                    prop="new"
                    :data="muni_data"
                    @click="
                        $router.push({
                            name: 'munidata',
                            params: { attribute: 'new', muni: muni },
                        })
                    "
                />
            </v-col>
            <v-col cols="2">
                <Mini
                    :color="attribute == 'active' ? '#1B9AAA' : '#e0e0e0'"
                    :dark="attribute == 'active'"
                    @click="
                        $router.push({
                            name: 'munidata',
                            params: { attribute: 'active', muni: muni },
                        })
                    "
                    title="Aktive Fälle"
                    no-details
                    :start="0"
                    prop="active"
                    :data="muni_data"
                />
            </v-col>
            <v-col cols="2">
                <Mini
                    :color="attribute == 'positive' ? '#1B9AAA' : '#e0e0e0'"
                    :dark="attribute == 'positive'"
                    @click="
                        $router.push({
                            name: 'munidata',
                            params: {
                                attribute: 'positive',
                                muni: muni,
                            },
                        })
                    "
                    title="Infektionen gesamt"
                    no-details
                    :start="0"
                    prop="positive"
                    :data="muni_data"
                />
            </v-col>
            <v-col cols="2">
                <Mini
                    :color="attribute == 'recovered' ? '#1B9AAA' : '#e0e0e0'"
                    :dark="attribute == 'recovered'"
                    @click="
                        $router.push({
                            name: 'munidata',
                            params: {
                                attribute: 'recovered',
                                muni: muni,
                            },
                        })
                    "
                    title="Genesen gesamt"
                    no-details
                    :start="0"
                    prop="recovered"
                    :data="muni_data"
                />
            </v-col>
            <v-col cols="2">
                <Mini
                    :color="attribute == 'deaths' ? '#1B9AAA' : '#e0e0e0'"
                    :dark="attribute == 'deaths'"
                    @click="
                        $router.push({
                            name: 'munidata',
                            params: { attribute: 'deaths', muni: muni },
                        })
                    "
                    title="Todesfälle gesamt"
                    no-details
                    :start="0"
                    prop="deaths"
                    :data="muni_data"
                />
            </v-col>
        </v-row>
        <v-row>
            <v-col cols="12" md="8"> </v-col>
            <!-- <v-col cols="4">
                <v-menu
                    ref="startMenu"
                    v-model="startMenu"
                    :close-on-content-click="false"
                    :return-value.sync="startDate"
                    transition="scale-transition"
                    offset-y
                    max-width="290px"
                    min-width="290px"
                >
                    <template v-slot:activator="{ on}">
                        <v-btn text dense v-on="on" class="pa-0 ma-0">
                            {{startDate.split("-")[1]}}/{{startDate.split("-")[0]}}
                        </v-btn> - 
                    </template>
                    <v-date-picker
                        v-model="startDate"
                        type="month"
                        no-title
                        scrollable
                    >
                        <v-spacer></v-spacer>
                        <v-btn text color="primary" @click="startMenu = false">
                            Cancel
                        </v-btn>
                        <v-btn
                            text
                            color="primary"
                            @click="saveStartDate(startDate)"
                        >
                            OK
                        </v-btn>
                    </v-date-picker>
                </v-menu>
                <v-menu
                    ref="endMenu"
                    v-model="endMenu"
                    :close-on-content-click="false"
                    :return-value.sync="endDate"
                    transition="scale-transition"
                    offset-y
                    max-width="290px"
                    min-width="290px"
                >
                    <template v-slot:activator="{ on, attrs }">
                        <v-btn text v-on="on" class="pa-0 ma-0">
                            {{endDate.split("-")[1]}}/{{endDate.split("-")[0]}}
                        </v-btn>
                    </template>
                    <v-date-picker
                        v-model="endDate"
                        type="month"
                        no-title
                        scrollable
                    >
                        <v-spacer></v-spacer>
                        <v-btn text color="primary" @click="endMenu = false">
                            Cancel
                        </v-btn>
                        <v-btn
                            text
                            color="primary"
                            @click="saveEndDate(endDate)"
                        >
                            OK
                        </v-btn>
                    </v-date-picker>
                </v-menu>
            </v-col> -->
        </v-row>
        <v-card class="ma-lg-3">
            <v-toolbar flat color="primary" dark>
                <v-toolbar-title>
                    <h2 class="text-xs-h6 text-lg-h4 font-weight-thin">
                        {{ titles[attribute] }} {{ muniDict[muni] }}
                    </h2>
                </v-toolbar-title>
            </v-toolbar>
            <canvas
                class="px-lg-10 pb-lg-5"
                :noheight="$vuetify.breakpoint.name == 'lg' || $vuetify.breakpoint.name == 'xl' ? 100 : 500"
                id="incidence-chart"
            ></canvas>
        </v-card>
        <v-card class="ma-3" flat>
            <v-toolbar flat dense>
                <v-toolbar-title primary-title> Datumsbereich </v-toolbar-title>
                <v-spacer></v-spacer>
                <v-btn
                    @click="setStart('all')"
                    small
                    depressed
                    class="mx-2"
                    color="#FFC43D"
                    >komplett</v-btn
                >
                <v-btn
                    @click="setStart('w2')"
                    small
                    depressed
                    class="mx-2"
                    color="#FFC43D"
                    >2. Welle</v-btn
                >
                <v-btn
                    @click="setStart('14tage')"
                    small
                    depressed
                    class="mx-2"
                    color="#FFC43D"
                    >14 Tage</v-btn
                >
            </v-toolbar>
            <v-card-text>
                <v-range-slider
                    v-model="dateRange"
                    min="0"
                    :max="muni_data && muni_data.incidence.length"
                >
                </v-range-slider>
            </v-card-text>
        </v-card>
        <div class="caption text-right">
            Stand {{ date }}<br />
            <span class="l1-line"></span> Lockdown Light, 2.11.2020<br />
            <span class="l2-line"></span> Weihnachts-Lockdown, 16.12.2020
        </div>
    </v-container>
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";
const moment = require("moment");
require("moment/locale/de");

import "chartjs-adapter-moment";

import { Annotation, LineAnnotation } from "chartjs-plugin-annotation";
import Mini from "@/components/charts/Mini.vue";

import axios from "axios";
import {
    Chart,
    LineController,
    BarController,
    BarElement,
    LineElement,
    PointElement,
    LinearScale,
    TimeScale,
    CategoryScale,
    Title,
    Tooltip,
    Filler,
    Legend,
} from "chart.js";
Chart.register(
    LineController,
    BarElement,
    BarController,
    PointElement,
    LineElement,
    LinearScale,
    TimeScale,
    CategoryScale,
    Title,
    Tooltip,
    Filler,
    Legend,
    Annotation,
    LineAnnotation
);

const API = process.env.VUE_APP_CORONA_API;

export default {
    props: {
        muni: String,
        attribute: String,
    },
    name: "IncidenceView",
    data: () => ({
        startMenu: false,
        startDate: new Date("2020-09-17").toISOString().substr(0, 7),
        endMenu: false,
        endDate: new Date().toISOString().substr(0, 7),
        dateRange: [180, 190],
        secondWave: true,
        myChart: null,
        chartTypes: {
            incidence: "line",
            new: "bar",
            active: "line",
            positive: "line",
            recovered: "line",
            deaths: "line",
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
            this.createChart("incidence-chart", this.chartData);
        }
    },
    watch: {
        dateRange(val) {
            this.render();
        },
        attribute(val) {
            this.render();
        },
        muni_data(val, oldval) {
            this.dateRange = [0, val.incidence.length];
            this.render();
        },
    },
    methods: {
        render() {
            if (this.muni_data) {
                const oldType = this.myChart && this.myChart.type;
                if (this.myChart) {
                    this.myChart.type = this.chartTypes[this.attribute];
                    this.myChart.data.datasets = this.chartData.data.datasets;
                    this.myChart.data.labels = this.chartData.data.labels;
                    this.myChart.options.plugins.annotation.annotations = this.annotations;
                    if (this.myChart.type != oldType) {
                        this.myChart.destroy();
                        this.createChart("incidence-chart", this.chartData);
                    } else {
                        this.myChart.update();
                    }
                } else {
                    this.createChart("incidence-chart", this.chartData);
                }
            }
        },
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
        //Incidence,
        Mini,
    },
    computed: {
        labelRange() {
            return this.muni_data["labels"].slice(
                this.dateRange[0],
                this.dateRange[1]
            );
        },
        dataSets() {
            switch (this.attribute) {
                case "incidence":
                    return [
                        {
                            // one line graph
                            label: "7-Tage-Inzidenz",
                            data: this.muni_data.incidence.slice(
                                this.dateRange[0],
                                this.dateRange[1]
                            ),
                            borderColor: "#1B9AAA",
                            backgroundColor: "rgba(0,0,0,0.1)",
                            pointHitRadius: 10,
                            pointBackgroundColor: "#1B9AAA",
                            pointBorderWidth: 0,
                            pointRadius: 0,
                            fill: true,
                            borderWidth: 2,
                        },
                    ];
                    break;
                case "new":
                    return [
                        {
                            type: "line",
                            label: "Durchschnittliche neue Fälle",
                            data: this.muni_data.average_new_cases.slice(
                                this.dateRange[0],
                                this.dateRange[1]
                            ),
                            borderColor: "#11B8A5",
                            backgroundColor: "#11B8A5",
                            pointRadius: 0,
                            pointBorderWidth: 0,
                            borderWidth: 5,
                        },
                        {
                            label: "Neue Fälle",
                            data: this.muni_data.new.slice(
                                this.dateRange[0],
                                this.dateRange[1]
                            ),
                            backgroundColor: "#FFC43D",
                            barPercentage: 0.5,
                            barThickness: 6,
                            maxBarThickness: 8,
                            minBarLength: 0,
                        },
                    ];
                    break;
                default:
                    return [
                        {
                            label: this.titles[this.attribute],
                            data: this.muni_data[this.attribute].slice(
                                this.dateRange[0],
                                this.dateRange[1]
                            ),
                            borderColor: "#1B9AAA",
                            backgroundColor: "rgba(27, 154, 170,0.3)",
                            pointHitRadius: 10,
                            pointBackgroundColor: "#1B9AAA",
                            pointBorderWidth: 0,
                            pointRadius: 0,
                            fill: true,
                            borderWidth: 2,
                        },
                    ];
                    break;
            }
        },
        annotations() {
            let annotations = {};
            switch (this.attribute) {
                case "incidence":
                    annotations = {
                        drawTime: "afterDatasetsDraw",
                        inc50: {
                            id: "hline1",
                            type: "line",
                            mode: "horizontal",
                            scaleID: "y",
                            value: "50",
                            borderColor: "#F78656",
                            borderWidth: 1,
                            label: {
                                backgroundColor: "#F78656",
                                content: "50",
                                enabled: true,
                                cornerRadius: 3,
                                position: "left",
                                xAdjust: 100,
                            },
                        },
                        inc200: {
                            id: "hline2",
                            type: "line",
                            mode: "horizontal",
                            scaleID: "y",
                            value: "200",
                            borderColor: "#EF476F",
                            borderWidth: 1,
                            label: {
                                backgroundColor: "#EF476F",
                                content: "200",
                                cornerRadius: 3,
                                enabled: true,
                                position: "left",
                                xAdjust: 100,
                            },
                        },
                    };
                    break;
                default:
                    break;
            }
            if (this.labelRange.includes("2020-11-02T07:30:00") > 0) {
                annotations["kontakt1"] = {
                    id: "k1",
                    type: "line",
                    mode: "vertical",
                    scaleID: "x",
                    value: new Date("02 Nov 2020"),
                    borderColor: "#F78656",
                    borderWidth: 3,
                    borderDash: [10, 10],
                    label: {
                        rotation: 0,
                        backgroundColor: "#F78656",
                        //content: "Lockdown Light",
                        enabled: true,
                        cornerRadius: 0,
                        position: "center",
                        yAdjust: 0,
                    },
                };
            }
            if (this.labelRange.includes("2020-12-16T07:30:00") > 0) {
                annotations["kontakt2"] = {
                    id: "k2",
                    type: "line",
                    mode: "vertical",
                    scaleID: "x",
                    value: new Date("16 Dec 2020"),
                    borderColor: "#F78656",
                    borderWidth: 3,
                    borderDash: [10, 10],
                    label: {
                        rotation: 0,
                        backgroundColor: "#F78656",
                        enabled: true,
                        cornerRadius: 0,
                        position: "center",
                        yAdjust: 0,
                    },
                };
            }
            return annotations;
        },
        chartData() {
            return {
                type: this.chartTypes[this.attribute],
                data: {
                    labels: this.labelRange,
                    datasets: this.dataSets,
                },
                options: {
                    responsive: true,
                    lineTension: 1,
                    scales: {
                        x: {
                            type: "time",
                            time: {
                                unit: "day",
                                displayFormats: {
                                    day: "DD. MMM",
                                },
                            },

                            beginAtZero: true,
                            ticks: {
                                padding: 25,
                            },
                        },

                        y: {
                            beginAtZero: true,
                            ticks: {
                                padding: 25,
                            },
                        },
                    },
                    plugins: {
                        legend: {
                            labels: {
                                usePointStyle: true,
                                boxWidth: 8,
                            },
                        },

                        annotation: {
                            events: ["click"],
                            annotations: this.annotations,
                            animation: {
                                numbers: {
                                    properties: ["width", "height"],
                                    type: "number",
                                },
                            },
                        },
                    },
                },
            };
        },
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
    border-top: 4px dashed #f78656;
    padding-top: 2px;
    width: 40px;
}
.l2-line {
    display: inline-block;
    border-top: 4px dashed #ef476f;
    padding-top: 2px;
    width: 40px;
}
</style>
