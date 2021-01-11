<template>
    <v-container
        fluid
        v-if="muni_data"
        class="d-flex child-flex flex-column pa-0"
    >
        <v-row no-gutters>
            <v-col cols="12">
                <div class="body-2 pt-5 px-9 black--text">
                    Zuletzt aktualisiert am {{ date }}
                </div>
            </v-col>
            <v-col cols="12" md=2 class="d-none d-md-flex">
                <v-list nav class="mt-4 pl-7" id="nav-list">
                    <v-list-item-group v-model="activeTab" active-class="nav-active">
                        <v-list-item
                            :ripple="false"
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
            <v-col cols="12" md=10>
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
                                        class="float-left text-h6 text-md-h5 font-weight-bold pl-0 black--text labelButton"
                                        disabled
                                    >
                                        Fallzahlen
                                    </v-btn>
                                    <v-btn
                                        color="primary"
                                        text
                                        dark
                                        v-on="on"
                                        class="text-h6 text-md-h5 font-weight-bold pa-0"
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
                        <v-menu offset-y bottom left v-if="false">
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
                    <v-row>
                        <v-card flat class="mx-6 pb-0" :width="attribute.width" :key="attribute.name"
                        v-for="attribute in keyAttributes
                        ">
                            <v-card-text
                                class="font-weight-bold caption pb-0 mt-0"
                            >
                                {{attribute.name}}
                            </v-card-text>
                            <v-card-text
                                class="font-weight-bold text-h3 mt-0 pt-0 pb-0 mb-0"
                            >
                                {{ Math.round(today[muni][attribute.item]) }}
                            </v-card-text>
                        </v-card>
                    </v-row>

                    <CoronaGraph
                        class="pb-8 mt-10 mx-0 px-0 mx-md-6"
                        title="Fälle nach Datum"
                        :dateRange="dateRange"
                        attribute="new"
                        cumulative="positive"
                        :muni="muni"
                    />
                    <CoronaGraph
                        class="pb-8 mt-10 mx-0 px-0 mx-md-6"
                        title="7-Tage-Inzidenz"
                        :dateRange="dateRange"
                        attribute="incidence"
                        :muni="muni"
                    />
                    <CoronaGraph
                        class="pb-8 mt-10 mx-0 px-0 mx-md-6"
                        title="Aktive Fälle"
                        :dateRange="dateRange"
                        attribute="active"
                        :muni="muni"
                    />
                    <CoronaGraph
                        class="pb-8 mt-10 mx-0 px-0 mx-md-6"
                        title="Todesfälle nach Datum"
                        :dateRange="dateRange"
                        attribute="new_deaths"
                        cumulative="deaths"
                        :muni="muni"
                    />
                    <div class="caption text-right py-5 px-2">
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
        keyAttributes: [
            {
                name: "Inzidenz",
                item: "incidence",
                width: 150
            },
            {
                name: "Aktive Fälle",
                item: "active",
                width: 150
            },
            {
                name: "Neue Fälle",
                item: "new",
                width: 150
            },
            {
                name: "Gesamzahl",
                item: "positive",
                width: 200
            },
        ],
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
<style scoped>
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
.labelButton >>> .v-btn__content {
    color: #023047 !important;
}
.nav-active:before {
    border-radius: 0 !important;
    opacity: 0;
}
.nav-active {
    border-radius: 0;
    background: #1B9AAA;
    color: white !important;
}
.nav-active .v-list-item__title {
    color: white !important;
    font-weight: bold;
}
#nav-list .v-list-item:before {
    border-radius: 0 !important;
}
</style>
