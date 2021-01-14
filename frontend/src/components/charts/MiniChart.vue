<template>
    <v-card
        color="#fff"
        tile
        @click.capture="$matomo.trackEvent('Corona', 'minichart-click', title)"
        :to="{ name: 'cases', params: { muni: muni } }"
    >
        <v-card-title class="text-h5 font-weight-bold text-uppercase">
            {{ title }}
        </v-card-title>
        <v-card-text class="mb-0 pt-0">
            Aktueller Wert
            <div class="value">
                <v-tooltip bottom max-width="300" color="rgba(0,0,0,1)">
                    <template v-slot:activator="{ on }">
                        <span v-on="on" class="ttip mr-4">{{ daily }}</span>
                    </template>
                    {{ description }}, Stand: {{ date }}
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
                            {{ lastWeekDifference }} ({{
                                lastWeekDifferencePercent
                            }}%)
                        </v-chip>
                    </template>
                    <span
                        >Differenz zum Wert vom
                        {{ lastWeekDate | moment("D.M.Y") }}</span
                    >
                </v-tooltip>
            </div>
        </v-card-text>
        <v-card-text class="mt-0 pt-2" v-if="sum">
            Summe der letzten 7 Tage
            <div class="value small">
                <v-tooltip
                    bottom
                    max-width="300"
                    color="rgba(0,0,0,1)"
                    v-if="sum"
                >
                    <template v-slot:activator="{ on }">
                        <span v-on="on" class="ttip mr-4">{{ lastWeek }}</span>
                    </template>
                    Die aufsummierten Werte der letzten 7 Tage vom
                    {{ lastWeekDate | moment("D.M.Y") }} bis
                    {{ nowDate | moment("D.M.Y") }}
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
                            {{ lastWeekDifference }} ({{
                                lastWeekDifferencePercent
                            }}%)
                        </v-chip>
                    </template>
                    <span
                        >Der Unterschied zur Summe der vorletzten 7 Tage.</span
                    >
                </v-tooltip>
            </div>
        </v-card-text>
        <v-card-text>
            <canvas
                :height="200"
                :id="`${attribute}-${muni}-overview-chart`"
            ></canvas>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
            <v-btn small text :to="{ name: 'cases', params: { muni: muni } }"
                >Alle Daten</v-btn
            >
        </v-card-actions>
    </v-card>
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";
import _ from "lodash";

require("moment/locale/de");
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
    Legend
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
    Legend
);

export default {
    props: {
        muni: {
            type: String,
            default: "sr"
        },
        title: String,
        description: String,
        attribute: String,
        sum: Boolean
    },
    methods: {
        createChart() {
            const ctx = document.getElementById(
                this.attribute + "-" + this.muni + "-overview-chart"
            );
            this.chart = new Chart(ctx, {
                type: "bar",
                data: this.chartData,
                options: this.chartOptions
            });
        }
    },
    data() {
        return {
            chart: null
        };
    },
    mounted() {
        this.createChart();
    },
    computed: {
        daily() {
            const data = this.allMuniData[this.muni][this.attribute];
            return Math.round(data[data.length - 1]);
        },
        nowDate() {
            const data = this.allMuniData[this.muni].labels;
            return data[data.length - 1];
        },
        lastWeekDate() {
            const data = this.allMuniData[this.muni].labels;
            return data[data.length - 8];
        },
        last2WeekDate() {
            const data = this.allMuniData[this.muni].labels;
            return data[data.length - 15];
        },
        lastWeek() {
            const data = this.allMuniData[this.muni][this.attribute];
            if (this.sum) {
                return Math.round(
                    data[data.length - 1] - data[data.length - 8]
                );
            } else {
                return Math.round(data[data.length - 1]);
            }
        },
        last2Week() {
            const data = this.allMuniData[this.muni][this.attribute];
            if (this.sum) {
                return Math.round(
                    data[data.length - 8] - data[data.length - 15]
                );
            } else {
                return Math.round(data[data.length - 8]);
            }
        },
        lastWeekDifference() {
            return this.lastWeek - this.last2Week;
        },
        lastWeekDifferencePercent() {
            const diff = this.lastWeek - this.last2Week;
            return Math.round((diff / this.last2Week) * 100, 2);
        },
        trend() {
            const diffPercent = this.lastWeekDifferencePercent
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
            const diffPercent = this.lastWeekDifferencePercent
            if (diffPercent > -5 && diffPercent < 5) {
                return "#e0e0e0"
            } else if (diffPercent <= -5) {
                return "#c3e5cc"
            }
            return "#f88"

        },
        muni_data() {
            return this.allMuniData[this.muni];
        },
        chartData() {
            const l = this.muni_data["labels"].length;
            const sets = [
                {
                    type: "line",
                    data: this.muni_data[this.attribute],
                    borderColor: "#11616A",
                    pointRadius: 0,
                    pointBorderWidth: 0,
                    borderWidth: 1
                },
                {
                    type: "bar",
                    data: this.muni_data[this.attribute],
                    borderWidth: 0,
                    backgroundColor: ctx => {
                        return ctx.index - l < -7 ? "transparent" : this.trendColor;
                    },
                    barPercentage: 6,
                    minBarLength: 0
                }
            ];
            return {
                labels: this.muni_data["labels"],
                datasets: sets
            };
        },
        chartOptions() {
            return {
                responsive: true,
                maintainAspectRatio: false,
                lineTension: 1,
                scales: {
                    x: {
                        type: "time",
                        gridLines: false,
                        time: {
                            unit: "month",
                            stepSize: 1.5,
                            displayFormats: {
                                month: "MMM"
                            }
                        },

                        beginAtZero: true,
                        ticks: {
                            padding: 25
                        }
                    },

                    y: {
                        display: false,
                        gridLines: false,
                        beginAtZero: true,
                        ticks: {
                            padding: 25
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        enabled: false
                    }
                }
            };
        },
        ...mapState({
            allMuniData: state => state.corona.allMuniData,

            muniDict: state => state.corona.muniDict,
            loaded: state => state.corona.loaded,
            munis: state => state.corona.munis,
            today: state => state.corona.today,
            yesterday: state => state.corona.yesterday,
            weekerday: state => state.corona.weekerday,
            date: state => state.corona.date
        })
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