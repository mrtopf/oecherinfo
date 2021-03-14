<template>
    <v-card color="#fff" flat :height="$vuetify.breakpoint.mdAndUp ? 400 : 300">
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
        data: {type: Array, default: []},
    },
    computed: {
        series() {
            return this.data.map((d) => { return {name: d.name, data: d.data, type: 'bar', color: d.color}})
        },

        options() {
            return {
                grid: {
                    left: 0,
                    right: 0,
                    bottom: 0,
                    containLabel: true,
                },
                legend: {
                    data: this.data.map( (d) => d.name)
                },
                tooltip: {
                    trigger: "axis",
                    axisPointer: {
                        type: 'shadow'
                    },
                    transitionDuration: 0,
                    formatter2: function(params) {
                        console.log(params)
                        const date = new Date(params[0].data[0]);
                        const formattedDate = format.formatTime(
                            "dd.MM.yyyy",
                            date
                        );
                        let output = `<h3>${formattedDate}</h3><hr style="margin: 5px 0">`;
                        for (const p of params) {
                            const n = p.data[1].toLocaleString("de-DE");
                            output += `${p.marker} ${p.seriesName}: <strong>${n}</strong><br>`;
                        }
                        return output;
                    }
                },

                xAxis: {
                    axisLabel: {
                        fontFamily: "JetBrains Mono",
                    },
                    type: "category",
                    data: this.labels,
                },
                yAxis: {
                    axisLabel: {
                        fontFamily: "JetBrains Mono"
                    },
                    type: "value",
                },
                series: this.series
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
    },
};
</script>

