<template>
    <v-card tile class="mb-10">
        <v-toolbar dark flat>
            <v-toolbar-title>Trends</v-toolbar-title>
        </v-toolbar>
        <v-simple-table
            dense
            small
            :class="
                $vuetify.breakpoint.smAndUp
                    ? 'overview-table'
                    : 'overview-table small'
            "
        >
            <template v-slot:default>
                <thead>
                    <tr>
                        <th class="text-left">Kommune</th>
                        <th class="text-left">Inz.</th>
                        <th class="text-left">Neu</th>
                        <th class="text-left">Aktiv</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="item in todayList" :key="item.muni">
                        <td v-if="item.muni == 'sr'">Städteregion</td>
                        <td v-else>
                            {{ item.municipality_name }}
                        </td>
                        <td>
                            {{ item.incidence }}
                            <v-icon
                                :color="item.incidence_avg_trend_color"
                                :size="$vuetify.breakpoint.smAndUp ? 14 : 9"
                                class="pa-0 pl-1 ma-0"
                                >{{ item.incidence_avg_trend_icon }}</v-icon
                            >
                        </td>
                        <td>
                            {{ item.new }}
                            <v-icon
                                :size="$vuetify.breakpoint.smAndUp ? 14 : 9"
                                class="pa-0 ma-0"
                                :color="item.new_avg_trend_color"
                                >{{ item.new_avg_trend_icon }}</v-icon
                            >
                        </td>
                        <td>
                            {{ item.active }}
                            <v-icon
                                :size="$vuetify.breakpoint.smAndUp ? 14 : 9"
                                class="pa-0 ma-0"
                                :color="item.active_avg_trend_color"
                                >{{ item.active_avg_trend_icon }}</v-icon
                            >
                        </td>
                    </tr>
                </tbody>
            </template>
        </v-simple-table>
        <v-divider></v-divider>
        <v-card-text class="caption">
            Die Pfeile geben den Langzeittrend wieder (7-Tage-Durchschnitt von
            vor 7 Tagen mit dem von jetzt)
        </v-card-text>
    </v-card>
</template>
<script>
import { mapState, mapActions, mapGetters } from "vuex";

export default {
    props: {
        selectedMuni: String,
    },
    computed: {
        todayListFiltered() {
            return _.filter(
                this.todayList,
                (item) => item.muni == "sr" || item.muni == this.selectedMuni
            );
        },
        ...mapGetters("corona", ["muniName", "muni_data", "todayList"]),
    },
};
</script>
<style lang="scss">
.overview-table {
    thead {
        tr  {
            background: #FFC43D;
            th {
                color: black !important;
                text-transform: uppercase;
            }
        }
    }
    &.small {
        tr th {
            font-size: 11px !important;
            padding: 0 10px !important;
        }
        td {
            font-size: 10px !important;
            padding: 0 10px !important;
        }
    }
}
</style>