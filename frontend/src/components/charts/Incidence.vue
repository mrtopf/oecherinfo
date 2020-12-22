<template>
    <v-card color="#F8FFE5" :loading="loading" tile>
        <v-tabs
            background-color="#11B8A5"
            center-active
            dark
            v-model="selected"
        >
            <v-tab key="incidence">Inzidenz</v-tab>
            <v-tab key="new">neue Fälle</v-tab>
            <v-tab>aktive Fälle</v-tab>
        </v-tabs>
        <v-card-text v-if="!loading">
            <div id="incidence-chart1">
                <apexchart
                    type="line"
                    height="400"
                    :options="chartOptions"
                    :series="series"
                ></apexchart>
            </div>
            <div id="brush-chart1">
                <apexchart
                    type="area"
                    height="130"
                    :options="chartOptionsLine"
                    :series="series"
                ></apexchart>
            </div>
        </v-card-text>
    </v-card>
</template>
<script>

export default {
    props: {
        chartData: Object,
        muniName: String,
        muni: String, // key of muni
        color: String,
        start: Number,
        dark: {
            type: Boolean,
            default: false,
        },
        loading: Boolean,
        no_animations: Boolean,
    },
    data: () => ({
        selected: "incidence",
        chart: null,
        brush_chart: null,
        cats: ["incidence", "new", "deaths"],
    }),
    computed: {
        seriesLine() {
            return [
                {
                    data: this.chartData[this.cats[this.selected]],
                },
            ];
        },
        series() {
            return [
                {
                    name: "7-Tage-Indidenz",
                    data: this.chartData[this.cats[this.selected]],
                },
            ];
        },
        chartOptionsLine() {
            const d = this.chartData["labels"];
            const lastDate = d[d.length - 1];

            return {
                chart: {
                    id: "brush-chart",
                    height: 130,
                    type: "area",
                    brush: {
                        target: "incidence-chart",
                        enabled: true,
                    },
                    selection: {
                        enabled: true,
                        xaxis: {
                            min: new Date("17 Sep 2020").getTime(),
                            max: new Date(lastDate).getTime(),
                        },
                    },
                    animations: {
                        enabled: false,
                    },
                },
                colors: ["#008FFB"],
                fill: {
                    type: "gradient",
                    gradient: {
                        opacityFrom: 0.91,
                        opacityTo: 0.1,
                    },
                },
                xaxis: {
                    type: "datetime",
                    categories: this.chartData["labels"],
                    tooltip: {
                        enabled: false,
                    },
                },
                yaxis: {
                    labels: {
                        formatter: function (value) {
                            return Math.round(value);
                        },
                    },
                    tickAmount: 3,
                },
            };
        },
        chartOptions() {
            const incidenceYAxes = [
                {
                    y: "50",
                    strokeDashArray: 0,
                    borderColor: "#EF476F",
                    label: {
                        offsetX: -5,
                        borderColor: "#EF476F",
                        style: {
                            color: "#fff",
                            background: "#EF476F",
                        },
                        text: "50",
                    },
                },
                {
                    y: "200",
                    strokeDashArray: 0,
                    borderColor: "#A90F33",
                    label: {
                        offsetX: -5,
                        borderColor: "#A90F33",
                        style: {
                            color: "#ffffff",
                            fontWeight: 700,
                            background: "#A90F33",
                        },
                        text: "200",
                    },
                },
            ];

            let res = {
                chart: {
                    id: "incidence-chart",
                    height: 400,
                    toolbar: {
                        show: false,
                    },
                    animations: {
                        enabled: !this.no_animations,
                    },
                    toolbar: {
                        autoSelected: "pan",
                        show: false,
                    },
                    locales: [de],
                    defaultLocale: "de",
                },
                xaxis: {
                    type: "datetime",
                    categories: this.chartData["labels"],
                    tickAmount: 10,
                },
                yaxis: {
                    labels: {
                        formatter: function (value) {
                            return Math.round(value);
                        },
                    },
                },
                markers: {
                    size: 0,
                },
                stroke: {
                    width: [2],
                    curve: "straight",
                },

                annotations: {
                    xaxis: [
                        {
                            x: new Date("02 Nov 2020").getTime(),
                            strokeDashArray: 0,
                            borderColor: "#11B8A5",
                            label: {
                                offsetX: 0,
                                offsetY: 150,
                                borderColor: "#11B8A5",
                                style: {
                                    color: "#fff",
                                    background: "#11B8A5",
                                },
                                text: "Kontaktbeschr.",
                            },
                        },
                    ],
                },
            };
            if (this.selected == 0) {
                res.annotations.yaxis = incidenceYAxes;
            }
            return res;
        },
    },
};
</script>