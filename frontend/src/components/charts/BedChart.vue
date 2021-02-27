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
        data: Object,
        name: String,
        startZoom: {
            type: [String],
            default: "1900-01-01"
        },
        endZoom: {
            type: [String],
            default: "3100-01-01"
        },
        showLines: Boolean
    },
    computed: {
        options() {
            let markLines = {
                animationDuration: 500,
                silent: true,
                symbol: "none",
                lineStyle: {
                    color: "#666"
                },
                data: [
                    {
                        xAxis: "2020-11-02",
                        name: "L1",
                        label: {
                            formatter: "{b}",
                            show: true
                        },

                        lineStyle: {
                            color: "#f78656",
                            width: 2
                        }
                    },
                    {
                        xAxis: "2020-12-16",
                        name: "L2",
                        label: {
                            formatter: "{b}",
                            show: true
                        },

                        lineStyle: {
                            color: "#ef476f",
                            width: 2
                        }
                    }
                ]
            };

            return {
                grid: {
                    left: 50
                },

                toolbox: {
                    itemSize: 20,
                    feature: {
                        dataZoom: {
                            yAxisIndex: "none",
                            title: {
                                zoom: "Vergrößern",
                                back: "Zurück"
                            }
                        },
                        restore: { title: "Zurücksetzen" },
                        saveAsImage: { title: "PNG" }
                    }
                },
                tooltip: {
                    trigger: "axis",
                    transitionDuration: 0,
                    axisPointer: {
                        animation: false
                    },
                    formatter: function(params) {
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
                    type: "time",
                    boundaryGap: false
                },
                yAxis: {
                    type: "value"
                },
                legend: {
                    data: ["belegt", "frei", "Gesamtzahl"]
                },
                dataZoom: [
                    {
                        type: "slider",
                        show: true,
                        realtime: true,
                        startValue: this.startZoom,
                        endvalue: this.endZoom,
                        xAxisIndex: [1, 0],
                        labelFormatter: function(value, valueStr) {
                            return format.formatTime("dd.MM.yyyy", value);
                        }
                    }
                ],
                series: [
                    {
                        name: "belegt",
                        type: "bar",
                        stack: "total",
                        color: "#f78656",
                        emphasis: {
                            focus: "series"
                        },
                        data: zip(this.labels, this.data.occupiedBeds)
                    },
                    {
                        name: "frei",
                        type: "bar",
                        stack: "total",
                        color: "#037758",
                        emphasis: {
                            focus: "series"
                        },
                        data: zip(this.labels, this.data.freeBeds)
                    },
                    {
                        name: "Gesamtzahl",
                        type: "line",
                        color: "#1C9FB0",
                        data: zip(this.labels, this.data.allBeds)
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

