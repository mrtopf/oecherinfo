<template>
    <v-card color="#fff" flat :height="$vuetify.breakpoint.mdAndUp ? 500 : 300">
        <v-chart
            :option="options"
            :init-options="initOptions"
            ref="bar"
            autoresize
        />
    </v-card>
</template>

<script>
import { filter, zip } from "lodash";
import { format } from "echarts";

export default {
    props: {
        labels: Array,
        data: Array,
        name: String
    },
    computed: {
        options() {
            return {
                grid: {
                    left: 70,
                    right: 80,
                    top: 20,
                    bottom: 30,
                },
                visualMap: {
                    top: 50,
                    right: 10,
                    min: 0,
                    max: 300,
                    calculable: true,
                    realtime: true,
                    inRange: {
                        color: [
                            "#00cf00",
                            "#1ad108",
                            "#35d311",
                            "#4fd519",
                            "#6ad721",
                            "#84d82a",
                            "#9eda32",
                            "#b9dc3a",
                            "#d3de42",
                            "#ede04b",
                            "#fce155",
                            "#f1e164",
                            "#e7e173",
                            "#dce082",
                            "#d2e090",
                            "#c7e09f",
                            "#bde0ae",
                            "#b2e0bd",
                            "#a8dfcb",
                            "#9ddfda",
                            "#93d0d7",
                            "#88b9ca",
                            "#7da1be",
                            "#728ab1",
                            "#6773a5",
                            "#5c5c98",
                            "#52458c",
                            "#472e7f",
                            "#3c1773",
                            "#310066"
                        ]
                    }
                },
                // #30f030, #ffffca, #310066
                tooltip: {
                    trigger: "item",
                    transitionDuration: 0,
                    formatter: function(params) {

                        const d = params.data
                        const date = new Date(d[0]);
                        const formattedDate = format.formatTime(
                            "dd.MM.yyyy",
                            date
                        );
                        let output = `<h3>${formattedDate}</h3><hr style="margin: 5px 0">`;
                        output += `${d[1]} Jahre: <strong>${d[2].toLocaleString("de-DE")}</strong>`
                        return output;
                    }
                },

                xAxis: {
                    axisLabel: {
                        fontFamily: "JetBrains Mono",
                        formatter: function(value, index) {
                            const date = new Date(value);
                            const formattedDate = format.formatTime(
                                "MM/yyyy",
                                date
                            );
                            return formattedDate;
                        }
                    },
                    type: "category"
                },
                yAxis: {
                    axisLabel: {
                        fontFamily: "JetBrains Mono"
                    },
                    type: "category",
                    data: this.labels
                },
                series: [
                    {
                        blurSize: 0,
                        name: this.name,
                        type: "heatmap",
                        data: this.data,
                        emphasis: {
                            itemStyle: {
                                borderColor: "#333",
                                borderWidth: 1
                            }
                        },
                        progressive: 1000,
                        animation: false
                    }
                ]
            };
        }
    },

    data() {
        return {
            initOptions: {
                renderer: "canvas",
                locale: "de"
            }
        };
    }
};
</script>

