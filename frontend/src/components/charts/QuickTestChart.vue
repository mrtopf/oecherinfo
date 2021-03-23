<template>
    <v-card>
        <v-card
            color="#fff"
            flat
            :height="$vuetify.breakpoint.mdAndUp ? 400 : 300"
        >
            <v-chart
                :option="options"
                :init-options="initOptions"
                ref="bar"
                autoresize
            />
        </v-card>
        <!-- <v-toolbar flat class="caption">
            <v-spacer></v-spacer>
            <v-switch dense label="logarithmische Darstellung" v-model="show_log"></v-switch>
        </v-toolbar> -->
    </v-card>
</template>

<script>
import { filter, zip } from "lodash";
import { format } from "echarts";

export default {
    props: {
        labels: Array,
        data: { type: Object, default: {} }
    },
    computed: {
        series() {
            const rate = {
                name: "Positivrate",
                data: zip(this.labels, this.data.rate_percent),
                type: "line",
                large: true,
                color: "#115F6A",
                symbol: "none",
                yAxisIndex: 1,
                lineStyle: {
                    width: 3
                }
            };
            const total = {
                name: "Negative Tests",
                data: zip(this.labels, this.data.negative),
                type: "bar",
                color: "#98FDD6",
                stack: 'amount',
                // label: {
                //     fontFamily: "JetBrains Mono",
                //     fontWeight: "bold",
                //     color: "#fff",
                //     show: true,
                //     position: "inside"
                // }
            };
            const positive = {
                stack: 'amount',
                name: "Positive Tests",
                data: zip(this.labels, this.data.positive),
                type: "bar",
                color: "#EF476F",
                // label: {
                //     fontFamily: "JetBrains Mono",
                //     fontWeight: "bold",
                //     distance: 3,
                //     show: true,
                //     position: "top"
                // }
            };
            return [total, positive, rate];
        },

        options() {
            return {
                grid: {
                    left: 0,
                    right: 20,
                    bottom: 0,
                    containLabel: true
                },
                legend: {
                    data: ["Negative Tests", "Positive Tests", "Positivrate"]
                },
                tooltip: {
                    trigger: "axis",
                    axisPointer: {
                        type: "shadow"
                    },
                    transitionDuration: 0,
                    formatter: function(params) {
                        const date = new Date(params[0].data[0]);
                        const formattedDate = format.formatTime(
                            "dd.MM.yyyy",
                            date
                        );
                        let output = `<h3>${formattedDate}</h3><hr style="margin: 5px 0">`;
                        for (const p of params) {
                            const n = p.data[1].toLocaleString("de-DE");
                            if (p.seriesIndex == 2) {
                                output += `${p.marker} ${p.seriesName}: <strong>${n}%</strong><br>`;
                            } else {
                                output += `${p.marker} ${p.seriesName}: <strong>${n}</strong><br>`;
                            }
                        }
                        return output;
                    }
                },

                xAxis: {
                    axisLabel: {
                        fontFamily: "JetBrains Mono",
                        formatter: function(value, valueStr) {
                            return format.formatTime("dd.MM.yyyy", value);
                        }
                    },
                    type: "time",
                    boundaryGap: false
                },
                yAxis: [
                    {
                        axisLabel: {
                            fontFamily: "JetBrains Mono",
                        },
                        name: "Anzahl",
                        type: this.show_log ? "log" : "value"
                    },
                    {
                        name: "Rate in %",
                        axisLabel: {
                            fontFamily: "JetBrains Mono"
                        },
                        type: "value",
                        max: 4
                    }
                ],
                series: this.series
            };
        }
    },

    data() {
        return {
            show_log: false,
            initOptions: {
                renderer: "canvas",
                locale: "de"
            }
        };
    }
};
</script>

