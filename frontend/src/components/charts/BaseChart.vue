<template>
    <v-card color="white" :loading="loading">
        <v-toolbar :color="color" :dark="dark" flat>
            <v-toolbar-title class="font-weight-thin text-uppercase text-h3">
                {{ title }}
            </v-toolbar-title>
        </v-toolbar>
        <v-card-text>
            <div :id="id"></div>
        </v-card-text>
    </v-card>
</template>
<script>
export default {
    props: {
        id: String,
        start: Number,
        data: Object,
        color: String,
        dark: {
            type: Boolean,
            default: false,
        },
        loading: Boolean,
        no_animations: Boolean,
        title: String,
        prop: String,
        chartColor: {
            type: String,
            default: "#2f2f2f",
        },
    },
    methods: {
        render() {
            this.chart = new ApexCharts(
                document.querySelector("#" + this.id),
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
            if (val) {
                this.chart.updateSeries([
                    {
                        name: this.title,
                        data: val[this.prop].slice(this.start, 99999),
                    },
                ]);
            }
        },
    },
    computed: {
        chartOptions() {
            return {
                series: [
                    {
                        name: this.title,
                        data: this.data[this.prop].slice(this.start, 99999),
                    },
                ],
                chart: {
                    id: this.id,
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
                colors: [this.chartColor],
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
                    width: [3],
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