<template>
    <v-card tile flat elevation="4">
        <v-simple-table id="corona-overview-table">
            <template v-slot:default>
                <thead>
                    <tr>
                        <th
                            class="text-left font-weight-bold text-uppercase body-1 black--text"
                        >
                            Kommune
                        </th>
                        <th
                            class="text-left font-weight-bold text-uppercase body-1 black--text"
                        >
                            7-Tage-Inzidenz
                        </th>
                        <th
                            class="text-left font-weight-bold text-uppercase body-1 black--text"
                        >
                            R-Wert 4 Tage
                        </th>
                        <th
                            class="text-left font-weight-bold text-uppercase body-1 black--text"
                        >
                            Positiv getestet
                        </th>
                        <th
                            class="text-left font-weight-bold text-uppercase body-1 black--text"
                        >
                            Aktive Fälle
                        </th>
                        <th
                            class="text-left font-weight-bold text-uppercase body-1 black--text"
                        >
                            Todesfälle
                        </th>
                    </tr>
                </thead>
                <tbody>
                    <tr
                        @click="handleMuniClick(muni.muni)"
                        v-for="muni in muniData"
                        :key="muni.muni"
                        :class="muni.muni == 'sr' ? 'totalRow' : ''"
                    >
                        <td class="link">{{ muni.name }}</td>
                        <td>
                            <v-badge
                                :color="getChipColor(muni.today.rollingRate)"
                                class="mr-4"
                            ></v-badge>
                            {{ muni.today.rollingRate }}
                            <v-icon
                                :color="muni.rollingRateTrend.color"
                                :size="$vuetify.breakpoint.smAndUp ? 14 : 9"
                                class="pa-0 pl-0 ma-0"
                                >{{ muni.rollingRateTrend.icon }}</v-icon
                            >
                        </td>
                        <td>{{ muni.today.r4 }}</td>
                        <td>
                            {{ muni.today.cumCases }}
                            <small>(+{{ muni.today.newCases }}) </small>
                            <v-icon
                                :color="muni.casesTrend.color"
                                :size="$vuetify.breakpoint.smAndUp ? 14 : 9"
                                class="pa-0 pl-0 ma-0"
                                >{{ muni.casesTrend.icon }}</v-icon
                            >
                        </td>
                        <td>
                            {{ muni.today.activeCases }}
                            <v-icon
                                :color="muni.activeTrend.color"
                                :size="$vuetify.breakpoint.smAndUp ? 14 : 9"
                                class="pa-0 pl-0 ma-0"
                                >{{ muni.activeTrend.icon }}</v-icon
                            >
                        </td>
                        <td @click.stop="handleMuniClick(muni.muni, 'deaths')">
                            {{ muni.today.cumDeaths || 0 }}
                            <small v-if="muni.today.newDeaths"
                                >(+{{ muni.today.newDeaths }})</small
                            >
                            <v-icon
                                :color="muni.deathsTrend.color"
                                :size="$vuetify.breakpoint.smAndUp ? 14 : 9"
                                class="pa-0 pl-0 ma-0"
                                >{{ muni.deathsTrend.icon }}</v-icon
                            >
                        </td>
                    </tr>
                </tbody>
            </template>
        </v-simple-table>
    </v-card>
</template>

<script>
import { map } from "lodash";

function computeTrend(v, min, max) {
    if (v < min) {
        return {
            icon: "fas fa-chevron-down",
            color: "green"
        };
    }
    if (v > max) {
        return {
            icon: "fas fa-chevron-up",
            color: "red"
        };
    }
    return {
        icon: "fa fa-minus",
        color: "grey"
    };
}

export default {
    props: {
        selectedMuni: String,
        data: Array
    },
    methods: {
        handleMuniClick(muni, section) {
            if (this.$matomo) {
                this.$matomo.trackEvent("Corona", "OverviewTable-Click", muni);
            }
            this.$router.push({
                name: section || "cases",
                params: {
                    muni: muni
                }
            });
        },
        getChipColor(incidence) {
            if (incidence > 200) {
                return "#960D2D";
            } else if (incidence > 50) {
                return "#F78656";
            }
            return "#05C793";
        }
    },
    computed: {
        muniData() {
            return map(this.data, function(v) {
                v["rollingRateTrend"] = computeTrend(
                    v.trend.rollingRate7DayChangePercent * 100,
                    -5,
                    5
                );
                v["casesTrend"] = computeTrend(
                    v.trend.cumCases7DayChangePercent * 100,
                    -5,
                    5
                );
                v["activeTrend"] = computeTrend(
                    v.trend.activeCases7DayChangePercent * 100,
                    -5,
                    5
                );
                v["deathsTrend"] = computeTrend(
                    v.trend.newDeaths7DayChangePercent * 100,
                    -5,
                    5
                );
                v["r4Trend"] = computeTrend(
                    v.trend.r47DayChangePercent * 100,
                    -5,
                    5
                );
                return v;
            });
        }
    },
    data() {
        return {};
    }
};
</script>
<style lang="scss">
.totalRow {
    background: #2f2f2f;
    color: white;
    font-weight: bold;
    td {
        background: #2f2f2f;
    }
}
#corona-overview-table {
    tr {
        cursor: pointer;
    }
    .link {
        text-decoration: underline;
    }
}
#corona-table .v-data-table-header tr {
    th {
        font-weight: bold;
        color: black;
        font-size: 14px !important;
    }
}
</style>
