<template>
    <v-container
        fluid
        v-if="muni_data"
        class="d-flex child-flex flex-column pa-0"
    >
        <v-row>
            <v-col cols="12">
                <div class="body-2 pt-5 px-9 black--text">
                    Zuletzt aktualisiert am {{ date }}
                </div>
            </v-col>
            <v-col cols="2">
                <v-list nav class="mt-0 pl-7">
                    <v-list-item-group v-model="activeTab">
                        <v-list-item
                            v-for="item in navItems"
                            :key="item.title"
                            link
                            :active="item.active"
                        >
                            <v-list-item-content>
                                <v-list-item-title class="primary--text">{{
                                    item.title
                                }}</v-list-item-title>
                            </v-list-item-content>
                        </v-list-item>
                    </v-list-item-group>
                </v-list>
            </v-col>
            <v-col cols="10">
                <v-card
                    class="ma-0 flex-grow-1 flex-shrink-0"
                    flat
                    ref="tabCard"
                >
                    <v-toolbar color="white" flat>
                        <v-toolbar-title
                            class="font-weight-bold text-uppercase"
                        >
                            <v-menu offset-y bottom left>
                                <template v-slot:activator="{ on }">
                                    <v-btn
                                        text
                                        class="float-left text-h5 font-weight-bold pl-0 black--text labelButton"
                                        disabled
                                    >
                                        Fallzahlen
                                    </v-btn>
                                    <v-btn
                                        color="primary"
                                        text
                                        dark
                                        v-on="on"
                                        class="text-h5 font-weight-bold pa-0"
                                    >
                                        {{ muniDict[muni] }}
                                        <v-icon right>fa fa-caret-down</v-icon>
                                    </v-btn>
                                </template>
                                <v-list dense nav>
                                    <v-list-item
                                        v-for="item in $store.state.corona
                                            .munis"
                                        :key="item.value"
                                        link
                                        :to="{
                                            name: 'munidata',
                                            params: {
                                                attribute: 'incidence',
                                                muni: item.muni,
                                            },
                                        }"
                                    >
                                        <v-list-item-content>
                                            <v-list-item-title>{{
                                                item.name
                                            }}</v-list-item-title>
                                        </v-list-item-content>
                                    </v-list-item>
                                </v-list>
                            </v-menu>
                        </v-toolbar-title>
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
                                <v-list-item
                                    class="font-weight-bold text-uppercase"
                                >
                                    <v-icon small left
                                        >fa fa-calendar-alt</v-icon
                                    >

                                    Zeitfenster
                                </v-list-item>
                                <v-divider></v-divider>
                                <v-list-item @click="setStart('all')"
                                    >komplett</v-list-item
                                >
                                <v-list-item @click="setStart('w2')"
                                    >2. Welle</v-list-item
                                >
                                <v-list-item @click="setStart('14tage')"
                                    >14 Tage</v-list-item
                                >
                            </v-list>
                        </v-menu>
                    </v-toolbar>
                    <v-divider></v-divider>
                    <!-- <v-tabs
                        centered
                        v-model="activeTab"
                        background-color="primary"
                        dark
                    >
                        <v-tab
                            exact
                            v-for="tab in Object.keys(tabs)"
                            :key="tab"
                        >
                            {{ tabs[tab] }}
                        </v-tab>
                    </v-tabs> -->
                    <!-- <v-card-text>
                        <div class="caption text-uppercase">
                            Wert am {{ date }}:
                        </div>
                        <div
                            class="text-h5 text-md-h3 font-weight-bold primary--text"
                        >
                            {{ todayValue
                            }}<v-tooltip top v-if="propName != 'recovered'">
                                <template v-slot:activator="{ on }">
                                    <v-icon
                                        v-on="on"
                                        :color="trend.color"
                                        :size="
                                            $vuetify.breakpoint.smAndUp
                                                ? 30
                                                : 12
                                        "
                                        :style="trend.rotate"
                                        class="pa-0 pl-1 pr-5 ma-0"
                                        >{{ trend.icon }}</v-icon
                                    >
                                </template>
                                <span>Langzeittrend</span>
                            </v-tooltip>
                            <small class="pl-3 text-md-h6 caption"
                                >{{ diffValue }} zum vorherigen Datum</small
                            >
                        </div>
                    </v-card-text> -->
                    <v-row>
                        <v-card flat class="mx-6 pb-0" width="150">
                            <v-card-text
                                class="font-weight-bold caption pb-0 mt-0"
                            >
                                Inzidenz
                            </v-card-text>
                            <v-card-text
                                class="font-weight-bold text-h3 mt-0 pt-0 pb-0 mb-0"
                            >
                                {{ Math.round(today[muni].incidence) }}
                            </v-card-text>
                        </v-card>
                        <v-card flat class="mx-6 pb-0" width="150">
                            <v-card-text
                                class="font-weight-bold caption pb-0 mt-0"
                            >
                                Aktive Fälle
                            </v-card-text>
                            <v-card-text
                                class="font-weight-bold text-h3 mt-0 pt-0"
                            >
                                {{ Math.round(today[muni].active) }}
                            </v-card-text>
                        </v-card>
                        <v-card flat class="mx-6 pb-0" width="150">
                            <v-card-text
                                class="font-weight-bold caption pb-0 mt-0"
                            >
                                Neu
                            </v-card-text>
                            <v-card-text
                                class="font-weight-bold text-h3 mt-0 pt-0 pb-0 mb-0"
                            >
                                {{ Math.round(today[muni].new) }}
                            </v-card-text>
                        </v-card>
                        <v-card flat class="mx-6 pb-0" width="200">
                            <v-card-text
                                class="font-weight-bold caption pb-0 mt-0"
                            >
                                Gesamtzahl
                            </v-card-text>
                            <v-card-text
                                class="font-weight-bold text-h3 mt-0 pt-0 pb-0 mb-0"
                            >
                                {{ Math.round(today[muni].positive) }}
                            </v-card-text>
                        </v-card>
                    </v-row>

                    <CoronaGraph
                        class="pb-8 mt-10 mx-6"
                        title="Fälle nach Datum"
                        :dateRange="dateRange"
                        attribute="new"
                        cumulative="positive"
                        :muni="muni"
                    />
                    <CoronaGraph
                        class="pb-8 mt-10 mx-6"
                        title="7-Tage-Inzidenz"
                        :dateRange="dateRange"
                        attribute="incidence"
                        :muni="muni"
                    />
                    <CoronaGraph
                        class="pb-8 mt-10 mx-6"
                        title="Aktive Fälle"
                        :dateRange="dateRange"
                        attribute="active"
                        :muni="muni"
                    />
                    <CoronaGraph
                        class="pb-8 mt-10 mx-6"
                        title="Todesfälle nach Datum"
                        :dateRange="dateRange"
                        attribute="new_deaths"
                        cumulative="deaths"
                        :muni="muni"
                    />
                    <v-divider></v-divider>
                    <div class="caption text-right py-5">
                        Stand {{ date }}<br />
                        <span class="l1-line"></span> Lockdown Light,
                        2.11.2020<br />
                        <span class="l2-line"></span> Weihnachts-Lockdown,
                        16.12.2020
                    </div>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";

import CoronaGraph from "@/components/CoronaGraph.vue";

export default {
    props: {
        muni: String,
        attribute: String,
    },
    name: "MuniView",
    data: () => ({
        activeTab: 0,
        startDate: new Date("2020-09-17").toISOString().substr(0, 7),
        endDate: new Date().toISOString().substr(0, 7),
        dateRange: [180, 190],
        tabs: {
            incidence: "Inzidenz",
            new: "neu",
            active: "aktiv",
            positive: "Fälle",
            recovered: "Genesen",
            deaths: "Tote",
        },
        navItems: [
            {
                title: "Übersicht",
            },
            {
                title: "Fallzahlen",
                active: true,
            },
            {
                title: "Genesen",
            },
            {
                title: "Todesfälle",
            },
        ],
    }),
    mounted() {
        if (this.muni_data) {
            this.dateRange = [0, this.muni_data.incidence.length];
        }
    },
    watch: {
        muni_data(val, oldval) {
            this.dateRange = [0, val.incidence.length];
        },
    },
    methods: {
        setStart(startSelected) {
            const end = this.muni_data.incidence.length;
            if (startSelected == "w2") {
                this.dateRange = [this.muni == "sr" ? 180 : 54, end];
            } else if (startSelected == "14tage") {
                this.dateRange = [end - 15, end];
            } else if (startSelected == "all") {
                this.dateRange = [0, end];
            } else {
                this.dateRange = [0, end];
            }
        },

        saveStartDate(date) {
            this.startDate = new Date(date);
        },
        saveEndDate(date) {
            this.endDate = new Date(date);
        },
        ...mapActions({
            updateMuni: "corona/updateMuni",
        }),
    },
    components: {
        CoronaGraph,
    },
    computed: {
        propName() {
            return Object.keys(this.tabs)[this.activeTab];
        },
        todayValue() {
            return Math.round(this.today[this.muni][this.propName]);
        },
        yesterdayValue() {
            return Math.round(this.yesterday[this.muni][this.propName]);
        },
        diffValue() {
            const v = this.todayValue - this.yesterdayValue;
            if (v > 0) {
                return "+" + v;
            } else if (v < 0) {
                return v;
            } else {
                return "+/- 0";
            }
        },
        trend() {
            const d = Math.round(
                this.today[this.muni][this.propName] -
                    this.weekerday[this.muni][this.propName]
            );
            if (d > 0) {
                return {
                    rotate: "padding-bottom: 0px; transform: rotate(45deg)",
                    icon: "fas fa-arrow-up",
                    color: "red",
                    hint: "Aufwärtstrend über 14 Tage",
                };
            } else if (d < 0) {
                return {
                    rotate: "transform: rotate(-45deg)",
                    icon: "fas fa-arrow-down",
                    color: "green",
                    hint: "Abwärtstrend über 14 Tage",
                };
            } else {
                return {
                    icon: "fas fa-minus",
                    color: "grey",
                    hint: "gleichbleibend über 14 Tage",
                };
            }
        },
        muni_data() {
            return this.allMuniData[this.muni];
        },
        ...mapGetters("corona", ["muniName"]),
        ...mapState({
            muniDict: (state) => state.corona.muniDict,
            loaded: (state) => state.corona.loaded,
            munis: (state) => state.corona.munis,
            allMuniData: (state) => state.corona.allMuniData,
            today: (state) => state.corona.today,
            yesterday: (state) => state.corona.yesterday,
            weekerday: (state) => state.corona.weekerday,
            date: (state) => state.corona.date,
        }),
    },
};
</script>
<style lang="scss">
.l1-line {
    display: inline-block;
    border-top: 3px dashed #f78656;
    padding-top: 2px;
    width: 40px;
}
.l2-line {
    display: inline-block;
    border-top: 3px dashed #ef476f;
    padding-top: 2px;
    width: 40px;
}
.legend {
    text-align: right;
    font-size: 0.7rem;
    color: black;
}
.labelButton .v-btn__content {
    color: #023047 !important;
}
</style>
