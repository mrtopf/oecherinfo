<template>
    <v-card
        color="#fff"
        class="ma-3 pa-3"
        tile
        :height="$vuetify.breakpoint.mdAndUp ? 650 : 480"
    >
        <v-card-text>
            <h2
                class="text-h6 text-md-h4 font-weight-bold primary--text pa-0 ma-0 mb-6"
            >
                {{ title }}: {{ todayValue }}
                <v-tooltip bottom max-width="300" v-if="trends">
                    <template v-slot:activator="{ on }">
                        <span v-on="on" class="mr-3 pa-0 ttip">
                            <small class="text-h6 text-md-h6 caption"
                                >{{ diffValueFormatted }}
                            </small>
                        </span>
                    </template>
                    Unterschied zum Vortag
                </v-tooltip>

                <v-tooltip bottom v-if="trends" max-width="300">
                    <template v-slot:activator="{ on }">
                        <span class="ttip">
                            <v-icon
                                v-on="on"
                                :color="trend.color"
                                :size="$vuetify.breakpoint.smAndUp ? 30 : 20"
                                :style="trend.rotate"
                                class="pa-0 pl-1 pr-5 ma-0 trend-icon"
                                >{{ trend.icon }}</v-icon
                            >
                        </span>
                    </template>
                    <span
                        >Der Langzeittrend ist die Differenz des Wertes von vor
                        7 Tagen verglichen mit dem aktuellen Wert.</span
                    >
                </v-tooltip>
            </h2>
            <v-card color="transparent" flat>
                <v-tabs
                    ref="tabs"
                    v-model="view"
                    background-color="#fff"
                    class="graph-tabs"
                    active-class="graph-tab-active"
                >
                    <v-tab
                        key="daily"
                        class="body-2 font-weight-bold"
                        @click="
                            $matomo.trackEvent(
                                'Corona',
                                'graphclick-daily',
                                attribute
                            )
                        "
                    >
                        Täglich
                    </v-tab>
                    <v-tab
                        key="cumulative"
                        v-if="cumulative"
                        @click="
                            $matomo.trackEvent(
                                'Corona',
                                'graphclick-cumulative',
                                attribute
                            )
                        "
                        class="body-2 font-weight-bold" > kumuliert
                    </v-tab>
                    <v-tab
                        key="data"
                        class="body-2 font-weight-bold"
                        @click="
                            $matomo.trackEvent(
                                'Corona',
                                'graphclick-data',
                                attribute
                            )
                        "
                    >
                        Daten
                    </v-tab>
                </v-tabs>
                <v-tabs-items v-model="view">
                    <v-tab-item eager>
                        <v-card
                            color="#fff"
                            flat
                            :height="$vuetify.breakpoint.mdAndUp ? 500 : 300"
                        >
                            <canvas
                                :height="
                                    $vuetify.breakpoint.mdAndUp ? 500 : 300
                                "
                                :id="`${attribute}-chart`"
                            ></canvas>
                        </v-card>
                    </v-tab-item>
                    <v-tab-item eager v-if="cumulative">
                        <v-card
                            color="#fff"
                            flat
                            :height="$vuetify.breakpoint.mdAndUp ? 500 : 300"
                        >
                            <canvas
                                :height="
                                    $vuetify.breakpoint.mdAndUp ? 500 : 300
                                "
                                :id="`${attribute}-cumulative-chart`"
                            ></canvas>
                        </v-card>
                    </v-tab-item>
                    <v-tab-item>
                        <v-card flat color="#fff">
                            <v-data-table
                                fixed-header
                                id="data-table"
                                must-sort
                                sort-by="date"
                                sort-desc
                                dense
                                disable-pagination
                                hide-default-footer
                                :headers="tableHeaders"
                                :items="tableData"
                                :height="
                                    $vuetify.breakpoint.mdAndUp ? 500 : 280
                                "
                            >
                                <template v-slot:item.date="item">
                                    {{ item.item.date | moment("D.M.Y") }}
                                </template>
                            </v-data-table>
                        </v-card>
                    </v-tab-item>
                </v-tabs-items>
            </v-card>
        </v-card-text>
    </v-card>
</template>
<script>
import { mapState, mapActions, mapGetters } from "vuex";

const moment = require("moment");
require("moment/locale/de");
import _ from "lodash";
import { Annotation, LineAnnotation } from "chartjs-plugin-annotation";
import "chartjs-adapter-moment";
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
    Legend
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
export default {
    props: {
        attribute: String,
        muni: String,
        cumulative: String, // attribute name of cumulative date or null
        title: String, // Title of the graph section
        trends: {
            type: Boolean,
            default: true
        },
        data: Object,
        barWidth: {
            type: Number,
            default: 1.8,
        }
    },
    data: () => ({
        view: 0,
        myChart: null,
        myCumulativeChart: null
    }),
    mounted() {
        if (this.muni_data) {
            this.createChart();
            this.createCumulativeChart();
        }
    },
    methods: {
        render() {
            if (this.muni_data) {
                if (this.myChart) {
                    this.myChart.data.datasets = this.chartData.data.datasets;
                    this.myChart.data.labels = this.chartData.data.labels;
                    this.myChart.options.plugins.annotation.annotations = this.annotations;
                    this.myChart.update();
                } else {
                    this.createChart();
                }
                if (this.myCumulativeChart) {
                    this.myCumulativeChart.data.datasets = this.cumulativeChartData.data.datasets;
                    this.myCumulativeChart.data.labels = this.cumulativeChartData.data.labels;
                    this.myCumulativeChart.options.plugins.annotation.annotations = this.annotations;
                    this.myCumulativeChart.update();
                } else {
                    this.createCumulativeChart();
                }
            }
        },
        createChart() {
            const ctx = document.getElementById(this.attribute + "-chart");
            this.myChart = new Chart(ctx, {
                type: "bar",
                data: this.chartData.data,
                options: this.chartData.options
            });
        },
        createCumulativeChart() {
            if (!this.cumulative) {
                return;
            }
            const ctx = document.getElementById(
                this.attribute + "-cumulative-chart"
            );
            this.myCumulativeChart = new Chart(ctx, {
                type: "bar",
                data: this.cumulativeChartData.data,
                options: this.chartData.options
            });
        },

        ...mapActions({
            updateMuni: "corona/updateMuni"
        })
    },
    computed: {
        /**
         * compute the moving average over the selected attribute, muni and date range
         */
        averages() {
            // get the date range
            const data = this.attributeData.slice(
                this.dateRange[0],
                this.dateRange[1]
            );

            function sum(numbers) {
                return _.reduce(numbers, (a, b) => a + b, 0);
            }

            function average(numbers) {
                return sum(numbers) / (numbers.length || 1);
            }

            function window(_number, index, array) {
                const start = Math.max(0, index - 3);
                const end = Math.min(array.length, index + 3);
                return _.slice(array, start, end);
            }

            return _.chain(data)
                .map(window)
                .map(average)
                .value();
        },
        attributeData() {
            return this.muni_data[this.attribute];
        },
        todayValue() {
            return Math.round(
                this.attributeData[this.attributeData.length - 1]
            );
        },
        diffValueWeek() {
            const data = this.attributeData;
            return Math.round(this.todayValue - data[data.length - 7]);
        },
        diffValue() {
            const data = this.attributeData;
            return Math.round(data[data.length - 1] - data[data.length - 2]);
        },
        diffValueFormatted() {
            const v = this.diffValue;
            if (v > 0) {
                return "+" + v;
            } else if (v < 0) {
                return v;
            } else {
                return "+/- 0";
            }
        },
        trend() {
            const d = this.diffValueWeek;
            if (d > 0) {
                return {
                    rotate:
                        "padding-bottom: 0px; transform: translate(0px,8px) rotate(45deg) ",
                    icon: "fas fa-arrow-up",
                    color: "red",
                    hint: "Aufwärtstrend über 14 Tage"
                };
            } else if (d < 0) {
                return {
                    rotate: "transform: rotate(-45deg)",
                    icon: "fas fa-arrow-down",
                    color: "green",
                    hint: "Abwärtstrend über 14 Tage"
                };
            } else {
                return {
                    icon: "fas fa-minus",
                    color: "grey",
                    hint: "gleichbleibend über 14 Tage"
                };
            }
        },
        tableHeaders() {
            let headers = [
                {
                    text: "Datum",
                    value: "date",
                    sortable: true,
                    sort: (a, b) => (new Date(a) < new Date(b) ? -1 : 1)
                },
                {
                    text: this.title,
                    value: "value",
                    sortable: true
                }
            ];
            if (this.cumulative) {
                headers.push({
                    text: "kumuliert",
                    value: "sum",
                    sortable: true
                });
            }
            return headers;
        },
        tableData() {
            const md = this.muni_data;
            let data = [];
            for (const idx in md["labels"]) {
                if (this.cumulative) {
                    data.push({
                        date: moment(md["labels"][idx]),
                        value: Math.round(md[this.attribute][idx]),
                        sum: md[this.cumulative][idx]
                    });
                } else {
                    data.push({
                        date: moment(md["labels"][idx]),
                        value: Math.round(md[this.attribute][idx])
                    });
                }
            }
            return data;
        },
        labelRange() {
            return this.muni_data["labels"].slice(
                this.dateRange[0],
                this.dateRange[1]
            );
        },
        dataSets() {
            const l = this.averages.length;
            return [
                {
                    type: "line",
                    label: "7-Tages-Durchschnitt",
                    data: this.averages,
                    borderColor: "#11616A",
                    pointRadius: 0,
                    pointBorderWidth: 0,
                    borderWidth: 3
                },
                {
                    label: this.title,
                    data: this.attributeData.slice(
                        this.dateRange[0],
                        this.dateRange[1]
                    ),
                    borderColor: "#ffffff",
                    borderWidth: this.$vuetify.breakpoint.mdAndUp ? 1 : 0,
                    backgroundColor: "#60D7E6",
                    //backgroundColor: (ctx) => {  return ctx.index -l < -7 ? "#fa0": "#0af"},

                    barPercentage: this.barWidth,
                    minBarLength: 0,
                    hoverBackgroundColor: "black"
                }
            ];
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
                            borderColor: "#333",
                            borderWidth: 1,
                            label: {
                                backgroundColor: "#E09D00",
                                content: "50",
                                enabled: true,
                                cornerRadius: 3,
                                position: "left",
                                xAdjust: 100
                            }
                        },
                        inc200: {
                            id: "hline2",
                            type: "line",
                            mode: "horizontal",
                            scaleID: "y",
                            value: "200",
                            borderColor: "#333",
                            borderWidth: 1,
                            label: {
                                backgroundColor: "#BC1038",
                                content: "200",
                                cornerRadius: 3,
                                enabled: true,
                                position: "left",
                                xAdjust: 100
                            }
                        }
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
                    borderColor: "#E09D00",
                    borderWidth: 2,
                    borderDash: [10, 10],
                    label: {
                        rotation: 0,
                        backgroundColor: "#E09D00",
                        //content: "Lockdown Light",
                        enabled: true,
                        cornerRadius: 0,
                        position: "center",
                        position: "top left",
                        yAdjust: 170,
                        content: "Lockdownchen"
                    }
                };
            }
            if (this.labelRange.includes("2020-12-16T15:00:00") > 0) {
                annotations["kontakt2"] = {
                    id: "k2",
                    type: "line",
                    mode: "vertical",
                    scaleID: "x",
                    value: new Date("16 Dec 2020"),
                    borderColor: "#BC1038",
                    borderWidth: 2,
                    borderDash: [10, 10],
                    label: {
                        rotation: 0,
                        backgroundColor: "#BC1038",
                        enabled: true,
                        cornerRadius: 0,
                        position: "bottom left",
                        yAdjust: 170,
                        content: "Lockdown"
                    }
                };
            }
            return annotations;
        },
        baseChartData() {
            return {
                type: "bar",
                data: {
                    labels: this.labelRange,
                    datasets: this.dataSets
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    lineTension: 1,
                    scales: {
                        x: {
                            type: "time",
                            time: {
                                unit: "month",
                                displayFormats: {
                                    month: "DD. MMM"
                                }
                            },

                            beginAtZero: true,
                            ticks: {
                                padding: 25
                            }
                        },

                        y: {
                            beginAtZero: true,
                            ticks: {
                                padding: 25
                            }
                        }
                    },
                    plugins: {
                        tooltip: {
                            backgroundColor: "#f0f0f0",
                            titleColor: "black",
                            bodyColor: "black",
                            footerColor: "black",
                            yPadding: 15,
                            xPadding: 15,
                            cornerRadius: 0,
                            borderColor: "#333333",
                            borderWidth: 1
                        },
                        legend: {
                            labels: {
                                usePointStyle: true,
                                boxWidth: 8
                            }
                        },

                        annotation: {
                            events: ["click"],
                            annotations: this.annotations,
                            animation: {
                                numbers: {
                                    properties: ["width", "height"],
                                    type: "number"
                                }
                            }
                        }
                    }
                }
            };
        },
        chartData() {
            let b = this.baseChartData;
            const myData = {
                type: "bar",
                data: {
                    labels: this.labelRange,
                    datasets: this.dataSets
                }
            };
            return { ...b, ...myData };
        },
        cumulativeChartData() {
            let b = this.baseChartData;
            const data = this.muni_data[this.cumulative];
            const dataSets = [
                {
                    label: this.title,
                    data: data,
                    borderColor: "#ffffff",
                    borderWidth: this.$vuetify.breakpoint.mdAndUp ? 1 : 0,
                    backgroundColor: "#1B9AAA",
                    barPercentage: 1.8,
                    minBarLength: 0,
                    hoverBackgroundColor: "black"
                }
            ];
            const myData = {
                type: "bar",
                data: {
                    labels: this.muni_data["labels"],
                    datasets: dataSets
                }
            };
            return { ...b, ...myData };
        },
        muni_data() {
            return this.data
            //return this.allMuniData[this.muni];
        },
        ...mapGetters("corona", ["muniName"]),
        ...mapState({
            muniDict: state => state.corona.muniDict,
            loaded: state => state.corona.loaded,
            munis: state => state.corona.munis,
            allMuniData: state => state.corona.allMuniData,
            today: state => state.corona.today,
            date: state => state.corona.date,
            dateRange: state => state.corona.dateRange
        })
    },
    watch: {
        // view(v) {
        //     console.log(v, this.$refs.tabs)
        //     this.$matomo.trackEvent('CoronaGraph', 'tab', this.attribute, v)
        // },
        dateRange(val) {
            this.render();
        },
        attribute(val) {
            this.render();
        },
        muni_data(val, oldval) {
            this.render();
        }
    }
};
</script>
<style lang="scss">
@import "~vuetify/src/styles/styles.sass";

#data-table {
    background: #f8f8f8 !important;
    padding-top: 5px;
}
#data-table thead th {
    background: #f8f8f8 !important;
    font-weight: bold;
    font-size: 14px;
}
.graph-tabs .v-tab {
    font-weight: bold;
}
.graph-tab-active {
    background: #ffc43d;
}
@media #{map-get($display-breakpoints, 'sm-and-down')} {
    .trend-icon {
        position: relative;
        top: -5px;
    }
}
</style>
