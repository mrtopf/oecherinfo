<template>
    <v-card
        color="#fff"
        tile
        @click.capture="
            $matomo && $matomo.trackEvent('Corona', 'minichart-click', title)
        "
        :to="{ name: 'cases', params: { muni: muni } }"
    >
        <v-card-title class="text-h5 font-weight-bold text-uppercase">
            {{ title }}
        </v-card-title>
        <v-card-text class="mb-0 pt-0">
            Aktueller Wert <small>(vor 7 Tagen)</small>
            <div class="value">
                <v-tooltip bottom max-width="300" color="rgba(0,0,0,1)">
                    <template v-slot:activator="{ on }">
                        <span v-on="on" class="ttip mr-4">{{ today }} <small>({{ today - weekChange }})</small></span>
                    </template>
                    {{ description }}, Stand: {{ dateFormatted }}
                </v-tooltip>

                <v-tooltip
                    bottom
                    max-width="300"
                    color="rgba(0,0,0,1)"
                    v-if="!sum"
                >
                    <template v-slot:activator="{ on }">
                        <v-chip
                            small
                            label
                            :color="trend.chipColor"
                            :text-color="trend.color"
                            v-on="on"
                        >
                            <v-icon
                                class="pr-3"
                                :color="trend.color"
                                :size="16"
                                >{{ trend.icon }}</v-icon
                            >
                            {{ weekChange }} ({{ weekChangePercent }}%)
                        </v-chip>
                    </template>
                    <span
                        >Differenz zum Wert vom {{ lastWeekDateFormatted }}:
                        {{ today - weekChange }}</span
                    >
                </v-tooltip>
            </div>
        </v-card-text>
        <v-card-text class="mt-0 pt-2" v-if="sum">
            Summe der letzten/vorletzten 7 Tage
            <div class="value small">
                <v-tooltip
                    bottom
                    max-width="300"
                    color="rgba(0,0,0,1)"
                    v-if="sum"
                >
                    <template v-slot:activator="{ on }">
                        <span v-on="on" class="ttip mr-4">{{ sumWeek }} / {{sum2Week}}</span>
                    </template>
                    Die aufsummierten Werte der letzten 7 Tage vom
                    {{ lastWeekDateFormatted }} bis
                    {{ dateFormatted }} sowie der 7 Tage davor.
                </v-tooltip>

                <v-tooltip bottom max-width="300" color="rgba(0,0,0,1)">
                    <template v-slot:activator="{ on }">
                        <v-chip
                            small
                            label
                            :color="trend.chipColor"
                            :text-color="trend.color"
                            v-on="on"
                        >
                            <v-icon
                                class="pr-3"
                                :color="trend.color"
                                :size="16"
                                >{{ trend.icon }}</v-icon
                            >
                            {{ weekChange }} ({{
                                weekChangePercent
                            }}%)
                        </v-chip>
                    </template>
                    <span
                        >Der Unterschied der Summe der letzten 7 Tage zur Summe der vorletzten 7 Tage.</span
                    >
                </v-tooltip>
            </div>
        </v-card-text>
        <v-card-text>
            <v-card color="#fff" flat :height="150">
                <v-chart
                    :option="options"
                    :init-options="initOptions"
                    ref="bar"
                    autoresize
                />
            </v-card>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
            <v-btn small color="gray" class="primary--text font-weight-bold" depressed :to="{ name: 'cases', params: { muni: muni } }"
                >Alle Daten ansehen</v-btn
            >
        </v-card-actions>
    </v-card>
</template>

<script>
import { format } from "echarts";

export default {
    props: {
        muni: {
            type: String,
            default: "sr"
        },
        title: String,
        description: String,
        attribute: String,
        data: Array,
        sum: Boolean,
        today: Number,
        sumWeek: Number,
        sum2Week: Number,
        weekChange: Number,
        weekChangePercent: Number,
        date: String,
        start: {type: [Number, String], default: 0},
    },
    methods: {},
    data() {
        return {
            initOptions: {
                renderer: "canvas",
                locale: "de"
            }
        };
    },
    mounted() {},
    computed: {
        dateFormatted() {
            return format.formatTime("dd.MM.yyyy", this.date);
        },
        lastWeekDateFormatted() {
            const lastWeekDate = new Date().setDate(
                new Date(this.date).getDate() - 7
            );
            return format.formatTime("dd.MM.yyyy", lastWeekDate);
        },
        lastWeek() {
            return this.today - this.weekChange
        },
        trend() {
            const diffPercent = this.weekChangePercent;
            if (diffPercent > -5 && diffPercent < 5) {
                return {
                    icon: "",
                    chipColor: "gray lighten-4",
                    color: "gray darken-3",
                    hint: "Gleichbleibend"
                };
            } else if (diffPercent <= -5) {
                // better times
                return {
                    icon: "fas fa-arrow-down",
                    chipColor: "green lighten-4",
                    color: "green darken-3",
                    hint: "Abwärtstrend über 14 Tage"
                };
            } else {
                // worse times
                return {
                    icon: "fas fa-arrow-up",
                    chipColor: "red lighten-4",
                    color: "red darken-3",
                    hint: "Aufwärtstrend über 14 Tage"
                };
            }
        },
        trendColor() {
            const diffPercent = this.weekChangePercent;
            if (diffPercent > -5 && diffPercent < 5) {
                return "#e0e0e0";
            } else if (diffPercent <= -5) {
                return "#c3e5cc";
            }
            return "#f88";
        },
        options() {
            return {
                grid: {
                    top: 0,
                    left: 0,
                    right: 0,
                    bottom: 0
                },
                xAxis: {
                    type: "category",
                    min: this.start,
                    show: false
                },
                yAxis: {
                    type: "value",
                    show: false
                },
                visualMap: {
                    type: "piecewise",
                    show: false,
                    dimension: 0,
                    seriesIndex: 0,
                    pieces: [
                        {
                            gt: this.data.length - 7,
                            lt: this.data.length,
                            color: this.trendColor,
                        },
                        {
                            gt: this.data.length-14,
                            lt: this.data.length-7,
                            color: this.sum ? "#f0f0f0":"#fff"
                        },
                    ]
                },

                series: [
                    {
                        areaStyle: {},
                        type: "line",
                        data: this.data,
                        smooth: 10.6,
                        lineStyle: {
                            color: "#11616A",
                            width: 2
                        }
                    }
                ]
            };
        }
    }
};
</script>
<style scoped>
.value {
    padding-top: 10px;
    font-size: 30px;
    color: black;
}
.value.small {
    font-size: 24px;
}
</style>