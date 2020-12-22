<template>
    <v-card color="white" :loading="loading">
        <v-toolbar :color="color" :dark="dark" flat>
            <v-toolbar-title class="font-weight-thin text-uppercase text-h3">
                Neue Fälle
            </v-toolbar-title>
        </v-toolbar>
        <v-card-text>
            <div id="new-cases-chart"></div>
        </v-card-text>
    </v-card>
</template>
<script>
export default {
    props: {
        start: Number,
        data: Object,
        color: String,
        dark: {
            type: Boolean,
            default: false,
        },
        loading: Boolean,
        no_animations: Boolean,
    },
    methods: {
        render() {
            this.chart = new ApexCharts(
                document.querySelector("#new-cases-chart"),
                this.chartOptions
            );
            this.chart.render();
        },
    },
    data: () => ({
        chart: null,
    }),
    mounted() {
        this.render();
    },
    watch: {
        data(val) {
            this.chart.updateSeries([
                {
                    name: "Neue Fälle",
                    data: this.data["new"].slice(this.start, 99999),
                },
                {
                    name: "Schnitt",
                    data: this.data["average_new_cases"].slice(
                        this.start,
                        99999
                    ),
                },
            ]);
        },
    },

    computed: {
        chartOptions() {
            return {
                series: [
                    {
                        name: "Neue Fälle",
                        data: this.data["new"].slice(this.start, 99999),
                    },
                    {
                        name: "Schnitt",
                        data: this.data["average_new_cases"].slice(
                            this.start,
                            99999
                        ),
                    },
                ],
                chart: {
                    id: "new-cases",
                    toolbar: {
                        show: false,
                    },
                    animations: {
                        enabled: true,
                    },
                    dropShadow: {
                        enabled: true,
                        enabledOnSeries: [1],
                        top: 5,
                        left: 0,
                        blur: 3,
                        opacity: 0.2,
                    },
                },
                colors: ["#fa0", "#85718D"],
                xaxis: {
                    categories: this.data["labels"].slice(this.start, 999999),
                    tickAmount: 10,
                },
                yaxis: {
                    labels: {
                        formatter: function (value) {
                            return Math.round(value);
                        },
                    },
                },
                stroke: {
                    width: [2, 4],
                    curve: "straight",
                },

                annotations: {
                    xaxis: [
                        {
                            x: "02. Nov",
                            strokeDashArray: 0,
                            borderColor: "#11B8A5",
                            label: {
                                offsetX: 0,
                                offsetY: -20,
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
        },
    },
};
</script>