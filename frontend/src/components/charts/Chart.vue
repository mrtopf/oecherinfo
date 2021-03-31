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
        color: {
            type: String,
            default: "#1C9FB0"
        },
        avgs: {
            type: Array,
            default: null
        },
        name: String,
        startZoom: {
            type: [String],
            default: "1900-01-01"
        },
        endZoom: {
            type: [String],
            default: "3100-01-01"
        },
        showLines: Boolean,
        showVisualMap: {type: String, default: ""}
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
            if (this.showLines) {
                markLines.data.push(
                    { yAxis: 50, lineStyle: {color: "#049F76"} }
                )
                markLines.data.push(
                    { yAxis: 100, lineStyle: {color: "#F78656"} }
                )
                markLines.data.push(
                    { yAxis: 200, lineStyle: {color: "#7D314E"} }
                )
            }

            let series = [
                {
                    name: this.name,
                    data: zip(this.labels, this.data),
                    type: "bar",
                    barWidth: "95%",
                    barCategoryGap: 0,
                    color: this.color,
                }
            ];
            
            series[0]["markLine"] = markLines;

            if (this.avgs) {
                series.push({
                    name: "7-Tage-Durchschnitt",
                    data: filter(zip(this.labels, this.avgs), v => v[1] != 0),
                    type: "line",
                    large: true,
                    color: "#11616A",
                    symbol: "none",
                    lineStyle: {
                        width: 3
                    }
                });
            }

            let visualMap;
            if (this.showVisualMap=="rollingRate") {
                visualMap = {
                    top: 50,
                    right: 10,
                    seriesIndex: 0,
                    show: this.$vuetify.breakpoint.mdAndUp,
                    // pieces: [
                    //     {
                    //         gt: 0,
                    //         lte: 50,
                    //         //color: "#037758"
                    //         color: "#06D6A0"
                    //     },
                    //     {
                    //         gt: 50,
                    //         lte: 100,
                    //         color: "#FFBC1F"
                    //     },
                    //     {
                    //         gt: 100,
                    //         lte: 200,
                    //         color: "#F78656"
                    //     },
                    //     {
                    //         gt: 200,
                    //         color: "#7D314E"
                    //     }
                    // ],
                    pieces: [
                        {
                            gt: 0,
                            lte: 50,
                            //color: "#037758"
                            color: "#1C9FB0"
                        },
                        {
                            gt: 50,
                            color: "#7D314E"
                        }
                    ],
                    outOfRange: {
                        color: "#999"
                    }
                };
            } else if (this.showVisualMap=="r") {
                visualMap = {
                    top: 50,
                    right: 10,
                    seriesIndex: 0,
                    show: this.$vuetify.breakpoint.mdAndUp,
                    pieces: [
                        {
                            gt: 0,
                            lte: 1,
                            color: "#1C9FB0"
                        },
                        {
                            gt: 1,
                            color: "#E9430C"
                        }
                    ],
                    outOfRange: {
                        color: "#999"
                    }
                };
            }

            return {
                grid: {
                    left: 40,
                    right: this.showVisualMap!="" ? 40 : 10,
                },
                toolbox: {
                    show: this.$vuetify.breakpoint.mdAndUp,
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
                visualMap: this.showVisualMap!="" ? visualMap : null,
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
                legend: {},
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
                series: series
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

