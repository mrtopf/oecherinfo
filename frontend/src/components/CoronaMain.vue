<template>
    <v-container fluid class="pa-0">
        <v-card tile flat>
            <v-card-title
                class="text-xs-h7 text-lg-h4 body-1 pb-0 font-weight-bold"
            >
                {{ muniName }}
                <v-menu offset-y bottom left>
                    <template v-slot:activator="{ on }">
                        <v-btn color="primary" dark icon v-on="on">
                            <v-icon>fa fa-caret-down</v-icon>
                        </v-btn>
                    </template>
                    <v-list dense nav>
                        <v-list-item
                            v-for="item in $store.state.corona.munis"
                            :key="item.value"
                            link
                            @click="updateMuni(item)"
                        >
                            <v-list-item-content>
                                <v-list-item-title>{{
                                    item.name
                                }}</v-list-item-title>
                            </v-list-item-content>
                        </v-list-item>
                    </v-list>
                </v-menu>
                <v-spacer></v-spacer>
                <v-menu offset-y bottom left>
                    <template v-slot:activator="{ on }">
                        <v-btn
                            color="oecheryellow darken-1"
                            dark
                            icon
                            v-on="on"
                        >
                            <v-icon>fa fa-calendar-alt</v-icon>
                        </v-btn>
                    </template>
                    <v-list>
                        <v-list-item class="font-weight-bold text-uppercase">
                            Zeitfenster
                        </v-list-item>
                        <v-divider></v-divider>
                        <v-list-item-group v-model="startSelected">
                            <v-list-item value="all"> komplett </v-list-item>
                            <v-list-item value="w2">2. Welle</v-list-item>
                            <v-list-item value="14tage">14 Tage</v-list-item>
                        </v-list-item-group>
                    </v-list>
                </v-menu>
            </v-card-title>
            <v-card-text class="pb-0 caption">
                <b>{{ startDict[startSelected] }}</b> | Stand: {{ date }}
            </v-card-text>

            <v-card-text class="py-0" v-if="loaded">
                <v-row class="text-center">
                    <v-col cols="12" md="4" order-md="3" order="1">
                        <v-card tile color="primary" class="text-left">
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
                                        <tr
                                            v-for="item in todayListFiltered"
                                            :key="item.muni"
                                        >
                                            <td v-if="item.muni == 'sr'">
                                                Städteregion
                                            </td>
                                            <td v-else>
                                                {{ item.municipality_name }}
                                            </td>
                                            <td>
                                                {{ item.incidence }}
                                                <v-icon
                                                    :color="
                                                        item.incidence_avg_trend_color
                                                    "
                                                    :size="
                                                        $vuetify.breakpoint
                                                            .smAndUp
                                                            ? 14
                                                            : 9
                                                    "
                                                    class="pa-0 pl-1 ma-0"
                                                    >{{
                                                        item.incidence_avg_trend_icon
                                                    }}</v-icon
                                                >
                                            </td>
                                            <td>
                                                {{ item.new }}
                                                <v-icon
                                                    :size="
                                                        $vuetify.breakpoint
                                                            .smAndUp
                                                            ? 14
                                                            : 9
                                                    "
                                                    class="pa-0 ma-0"
                                                    :color="
                                                        item.new_avg_trend_color
                                                    "
                                                    >{{
                                                        item.new_avg_trend_icon
                                                    }}</v-icon
                                                >
                                            </td>
                                            <td>
                                                {{ item.active }}
                                                <v-icon
                                                    :size="
                                                        $vuetify.breakpoint
                                                            .smAndUp
                                                            ? 14
                                                            : 9
                                                    "
                                                    class="pa-0 ma-0"
                                                    :color="
                                                        item.active_avg_trend_color
                                                    "
                                                    >{{
                                                        item.active_avg_trend_icon
                                                    }}</v-icon
                                                >
                                            </td>
                                        </tr>
                                    </tbody>
                                </template>
                            </v-simple-table>
                        </v-card>
                    </v-col>
                    <v-col cols="12" lg="4" order="1">
                        <Mini
                            :oldValue="yesterday[selectedMuni].incidence"
                            :newValue="today[selectedMuni].incidence"
                            :yesterdate="yesterdate"
                            color="#1B9AAA"
                            title="Inzidenz"
                            dark
                            @click="
                                $router.push({
                                    name: 'munidata',
                                    params: {
                                        attribute: 'incidence',
                                        muni: selectedMuni,
                                    },
                                })
                            "
                            :start="startIndex"
                            :loading="!loaded"
                            prop="incidence"
                            :data="muni_data"
                        />
                    </v-col>
                    <v-col cols="12" lg="4" order="2">
                        <Mini
                            :oldValue="yesterday[selectedMuni].active"
                            :newValue="today[selectedMuni].active"
                            :yesterdate="yesterdate"
                            color="#1B9AAA"
                            title="Aktiv"
                            dark
                            :start="startIndex"
                            :loading="!loaded"
                            prop="active"
                            :data="muni_data"
                            @click="
                                $router.push({
                                    name: 'munidata',
                                    params: {
                                        attribute: 'active',
                                        muni: selectedMuni,
                                    },
                                })
                            "
                        />
                    </v-col>

                    <v-col cols="12" md="4" order="5">
                        <Mini
                            :oldValue="yesterday[selectedMuni].positive"
                            :newValue="today[selectedMuni].positive"
                            :yesterdate="yesterdate"
                            small
                            color="#85718D"
                            title="Fälle"
                            dark
                            :start="startIndex"
                            :loading="!loaded"
                            prop="positive"
                            :data="muni_data"
                            @click="
                                $router.push({
                                    name: 'munidata',
                                    params: {
                                        attribute: 'positive',
                                        muni: selectedMuni,
                                    },
                                })
                            "
                        />
                    </v-col>
                    <v-col cols="12" md="4" order="6">
                        <Mini
                            :oldValue="yesterday[selectedMuni].recovered"
                            :newValue="today[selectedMuni].recovered"
                            :yesterdate="yesterdate"
                            small
                            dark
                            color="#11B8A5"
                            title="Genesen"
                            :start="startIndex"
                            :loading="!loaded"
                            prop="recovered"
                            :data="muni_data"
                            @click="
                                $router.push({
                                    name: 'munidata',
                                    params: {
                                        attribute: 'recovered',
                                        muni: selectedMuni,
                                    },
                                })
                            "
                        />
                    </v-col>
                    <v-col cols="12" md="4" order="7">
                        <Mini
                            :oldValue="yesterday[selectedMuni].deaths"
                            :newValue="today[selectedMuni].deaths"
                            :yesterdate="yesterdate"
                            small
                            color="#2f2f2f"
                            title="Todesfälle"
                            dark
                            :start="startIndex"
                            :loading="!loaded"
                            prop="deaths"
                            :data="muni_data"
                            @click="
                                $router.push({
                                    name: 'munidata',
                                    params: {
                                        attribute: 'deaths',
                                        muni: selectedMuni,
                                    },
                                })
                            "
                        />
                    </v-col>
                </v-row>
            </v-card-text>
            <v-card-text>
                <v-row>
                    <v-col cols="12" md="6">
                        <v-btn
                            x-large
                            color="primary"
                            dark
                            class="font-weight-bold"
                            elevation="2"
                            @click="
                                $router.push({
                                    name: 'munidata',
                                    params: {
                                        attribute: 'active',
                                        muni: selectedMuni,
                                    },
                                })
                            "
                        >
                            <v-icon left> fas fa-chevron-right </v-icon>
                            Alle Daten für {{ muniName }}</v-btn
                        >
                    </v-col>
                    <v-col class="text-right caption">
                        <b class="black--text">Stand {{ date }}</b> |
                        <span v-if="startSelected == 'w2'">
                            Es werden Daten der zweiten Welle ab 17. September
                            2020 angezeigt
                        </span>
                        <span v-if="startSelected == 'all'">
                            Es werden Daten seit Erfassungsbeginn angezeigt
                            (5.8.2020 für Kommunen, 21.3. für die Städteregion).
                        </span>
                        <span v-if="startSelected == '14tage'">
                            Es werden Daten der letzten 2 Wochen angezeigt.
                        </span>
                        <p>
                            Die Daten kommen aus dem
                            <a
                                target="_blank"
                                href="https://offenedaten.aachen.de/dataset/aktuelle-lage-zum-corona-virus"
                                >Open Data Portal der Stadt Aachen</a
                            >.
                        </p>
                    </v-col>
                </v-row>
            </v-card-text>

            <v-card-text class="mt-10">
                <h3 class="text-h4 black--text text-uppercase my-3">
                    Tabellarische Übersicht
                </h3>

                <v-card tile flat elevation="4">
                    <v-data-table
                        :headers="headers"
                        :items="todayList"
                        item-key="municipality"
                        :items-per-page="20"
                        item-class="rowClass"
                        hide-default-footer
                        :custom-sort="sortTable"
                        id="corona-table"
                        @click:row="handleMuniClick"
                    >
                        <template v-slot:item.active="{ item }">
                            {{ item.active }}
                            <small v-if="item.active_diff < 0">
                                ({{ item.active_diff }})
                            </small>
                            <small v-if="item.active_diff > 0">
                                (-{{ item.active_diff }})
                            </small>
                        </template>
                        <template v-slot:item.recovered="{ item }">
                            {{ item.recovered }}
                            <small v-if="item.recovered_diff < 0">
                                ({{ item.recovered_diff }})
                            </small>
                            <small v-if="item.recovered_diff > 0">
                                (+{{ item.recovered_diff }})
                            </small>
                        </template>
                        <template v-slot:item.incidence="{ item }">
                            <v-chip
                                :color="getChipColor(item.incidence)"
                                :dark="item.incidence > 200"
                            >
                                {{ item.incidence }}
                                <small v-if="item.incidence_diff > 0">
                                    (+{{ item.incidence_diff }})
                                </small>
                                <small v-if="item.incidence_diff < 0">
                                    ({{ item.incidence_diff }})
                                </small>
                            </v-chip>
                        </template>
                    </v-data-table>
                </v-card>
            </v-card-text>
        </v-card>
    </v-container>
</template>

<script>
import Mini from "./charts/Mini.vue";
import Incidence from "./charts/Incidence.vue";
import NewCases from "./charts/NewCases.vue";
import MiniNew from "./charts/MiniNew.vue";
import { mapState, mapActions, mapGetters } from "vuex";

import axios from "axios";

import _ from "lodash";

const API = process.env.VUE_APP_CORONA_API;

export default {
    name: "CoronaMain",
    data: () => ({
        range: [0, 100],
        startSelected: "w2",
        // diff sr to rest: 180-54
        startDict: {
            all: "Gesamtzeitraum",
            w2: "2. Welle",
            "14tage": "14 Tage",
        },
        secondWave: true,
        headers: [
            {
                text: "Kommune",
                align: "start",
                sortable: true,
                value: "municipality_name",
            },
            { text: "Aktiv", value: "active" },
            { text: "Neue Fälle", value: "new" },
            { text: "Fälle insgesamt", value: "positive" },
            { text: "Genesen", value: "recovered" },
            { text: "Verstorben", value: "deaths" },
            { text: "Inzidenz", value: "incidence" },
        ],
    }),
    methods: {
        handleMuniClick(item) {
            this.$router.push({
                name: "munidata",
                params: {
                    attribute: "incidence",
                    muni: item.muni,
                },
            });
        },
        getChipColor(incidence) {
            if (incidence > 200) {
                return "#EF476F";
            } else if (incidence > 50) {
                return "#FFC43D";
            }
            return "#7FEBC3";
        },
        sortTable(items, sortBy, sortDesc) {
            // this mainly keeps the SR element on bottom
            const parts = _.partition(items, (o) => o.muni == "sr"); // split into sr or not
            const d = sortDesc[0] ? "desc" : "asc";
            let result = _.orderBy(parts[1], [sortBy], [d]);
            result.push(parts[0][0]);
            return result;
        },
        ...mapActions({
            updateMuni: "corona/updateMuni",
        }),
    },
    async mounted() {},
    components: {
        Mini,
        MiniNew,
        Incidence,
        NewCases,
    },
    computed: {
        startIndex() {
            if (this.startSelected == "w2") {
                return this.selectedMuni == "sr" ? 180 : 54;
            } else if (this.startSelected == "14tage") {
                const l = this.muni_data["incidence"].length;
                return l - 14;
            } else {
                return 1;
            }
        },
        todayListFiltered() {
            return _.filter(
                this.todayList,
                (item) => item.muni == "sr" || item.muni == this.selectedMuni
            );
        },
        todayList() {
            // return today as list
            let res = [];
            for (const muni in this.today) {
                const tData = this.today[muni];
                const yData = this.yesterday[muni];
                const wData = this.weekerday[muni];
                let rec = {
                    municipality_name: tData["municipality_name"],
                    muni: tData["municipality"],
                };
                if (muni == "sr") {
                    rec["rowClass"] = "totalRow";
                    rec["municipality_name"] = "Gesamtergebnis";
                }
                for (const prop of [
                    "new",
                    "active",
                    "incidence",
                    "deaths",
                    "recovered",
                    "positive",
                    "new_avg",
                    "active_avg",
                    "incidence_avg",
                    "deaths_avg",
                    "recovered_avg",
                    "positive_avg",
                ]) {
                    rec[prop] = Math.round(tData[prop]);
                    rec[prop + "_diff"] = Math.round(tData[prop] - yData[prop]);

                    // compute trends via data from week ago
                    const d = Math.round(tData[prop] - wData[prop]);
                    if (d > 0) {
                        rec[prop + "_trend_color"] = "red";
                        rec[prop + "_trend_icon"] = "fas fa-chevron-up";
                    } else if (d < 0) {
                        rec[prop + "_trend_color"] = "green";
                        rec[prop + "_trend_icon"] = "fas fa-chevron-down";
                    } else {
                        rec[prop + "_trend_color"] = "grey";
                        rec[prop + "_trend_icon"] = "fa fa-minus";
                    }
                }
                res.push(rec);
            }
            return res;
        },
        ...mapGetters("corona", ["muniName", "muni_data"]),
        ...mapState({
            muniDict: (state) => state.corona.muniDict,
            loaded: (state) => state.corona.loaded,
            munis: (state) => state.corona.munis,
            today: (state) => state.corona.today,
            yesterday: (state) => state.corona.yesterday,
            weekerday: (state) => state.corona.weekerday,
            date: (state) => state.corona.date,
            yesterdate: (state) => state.corona.yesterdate,
            selectedMuni: (state) => state.corona.selectedMuni,
        }),
    },
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
#corona-table {
    tr {
        cursor: pointer;
    }
}
#corona-table .v-data-table-header tr {
    th {
        font-weight: bold;
        color: black;
        font-size: 14px !important;
    }
}
.overview-table {
    &.small {
        tr th {
            font-size: 11px !important;
            padding: 0 10px !important;
        }
        td {
            font-size: 11px !important;
            padding: 0 10px !important;
        }
    }
}
</style>
