<template>
    <div>
        <canvas
            :height="$vuetify.breakpoint.mdAndUp ? 500 : 300"
            :id="`${attribute}-chart`"
        ></canvas>
        <!-- <v-btn @click="rerender">render</v-btn> -->
    </div>
</template>
<script>
import { mapState, mapActions, mapGetters } from "vuex";

const moment = require("moment");
require("moment/locale/de");
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
export default {
    props: {
        attribute: String,
        muni: String,
        dateRange: Array,
        // chartHeight: [String, Number],
        // chartWidth: Number,
    },
    data: () => ({
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
            this.createChart(this.attribute + "-chart", this.chartData);
        }
    },
    // created: function () {
    //     window.addEventListener("resize", this.rerender);
    // },
    // beforeDestroy: function () {
    //     window.removeEventListener("resize", this.rerender);
    // },
    methods: {
        rerender() {
            this.myChart.destroy();
            this.myChart = null;
            this.$nextTick(function() {
                this.render();
            })
        },
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
                        this.createChart(
                            this.attribute + "-chart",
                            this.chartData
                        );
                    } else {
                        this.myChart.update();
                    }
                } else {
                    this.createChart(this.attribute + "-chart", this.chartData);
                }
            }
        },
        createChart(chartId, chartData) {
            const ctx = document.getElementById(this.attribute + "-chart");
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
                    borderWidth: 2,
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
            if (this.labelRange.includes("2020-12-16T15:00:00") > 0) {
                annotations["kontakt2"] = {
                    id: "k2",
                    type: "line",
                    mode: "vertical",
                    scaleID: "x",
                    value: new Date("16 Dec 2020"),
                    borderColor: "#ef476f",
                    borderWidth: 2,
                    borderDash: [10, 10],
                    label: {
                        rotation: 0,
                        backgroundColor: "#ef476f",
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
                    // aspectRatio: 2,
                    maintainAspectRatio: false,
                    lineTension: 1,
                    scales: {
                        x: {
                            type: "time",
                            time: {
                                unit: "day",
                                stepSize: 7,
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
    watch: {
        chartHeight(v) {
            console.log("height", v);
            if (this.myChart) {
                this.myChart.destroy();
            }
            this.render();
            //this.myChart.canvas.parentNode.style.height=v
        },
        chartWidth(v) {
            console.log("width", v);
            if (this.myChart) {
                console.log("bye");
                this.myChart.destroy();
                this.myChart = null;
            }
            this.$nextTick(function () {
                this.render();
            });

            //this.myChart.canvas.parentNode.style.height=v
        },
        dateRange(val) {
            this.render();
        },
        attribute(val) {
            this.render();
        },
        muni_data(val, oldval) {
            this.render();
        },
    },
};
</script>