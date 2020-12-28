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
                <v-btn icon :loading="!loaded" @click="load()">
                    <v-icon color="secondary">fa fa-sync</v-icon>
                </v-btn>
            </v-card-title>
            <v-card-text class="pb-0 caption">
                <b>{{ startDict[startSelected] }}</b> | Stand: {{ date }}
            </v-card-text>

            <v-card-text class="py-0" v-if="loaded">
                <v-row>
                    <!-- graphs -->
                    <v-col cols="12" md="8" order="2" order-md="1">
                        <v-row>
                            <v-col cols="12" md="6">
                                <Mini
                                    :oldValue="
                                        yesterday[selectedMuni].incidence
                                    "
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
                            <v-col cols="12" md="6">
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

                            <v-col cols="12" md="6">
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
                            <v-col cols="12" md="6">
                                <Mini
                                    :oldValue="
                                        yesterday[selectedMuni].recovered
                                    "
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
                            <v-col cols="12" md="6">
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
                            <v-col cols="12" md="6">
                                <Mini
                                    :oldValue="yesterday[selectedMuni].new"
                                    :newValue="today[selectedMuni].new"
                                    :yesterdate="yesterdate"
                                    small
                                    color="#ef476f"
                                    title="Neue Fälle"
                                    dark
                                    :start="startIndex"
                                    :loading="!loaded"
                                    prop="new"
                                    :data="muni_data"
                                    @click="
                                        $router.push({
                                            name: 'munidata',
                                            params: {
                                                attribute: 'new',
                                                muni: selectedMuni,
                                            },
                                        })
                                    "
                                />
                            </v-col>
                        </v-row>
                    </v-col>
                    <v-col cols="12" md="4" order="1" order_md="2" class="mt-3">
                        <TrendTable :selectedMuni="selectedMuni" />
                    </v-col>
                </v-row>
            </v-card-text>
            <v-card-text v-if="loaded">
                <v-row>
                    <v-col cols="12" md="4">
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
            <v-card-text class="mb-5">
                <v-list>
                    <v-list-item>
                        <v-list-item-icon>
                 <v-icon large color="#1B9AAA">fa fa-info-circle</v-icon>

                        </v-list-item-icon>
                        <v-list-item-content class="caption text-md-body-1 ">
                Aktuelle Informationen zum Corona-Virus inklusive der gerade
                gültigen Verordnungen der Städteregion Aachen findet man unter
                <b><a
                    target="_blank"
                    href="https://www.staedteregion-aachen.de/corona"
                    >
                    www.staedteregion-aachen.de/corona</a
                ></b>

                        </v-list-item-content>
                    </v-list-item>
                </v-list>
            </v-card-text>
            <v-divider></v-divider>
            <v-card-text class="mt-5">
                <h3 class="text-h6 text-md-h4 black--text text-uppercase my-3">
                    Situation der Krankenhäuser in der Städteregion
                </h3>
                <hospital-table></hospital-table>
            </v-card-text>
            <v-divider></v-divider>

            <v-card-text class="mt-10" v-if="loaded">
                <h3 class="text-h6 text-md-h4 black--text text-uppercase my-3">
                    Tabellarische Übersicht
                </h3>
                <OverviewTable></OverviewTable>
            </v-card-text>
            <!-- <v-card-text class="mt-10" v-if="loaded">
                <h3 class="text-h4 black--text text-uppercase my-3">
                    Weiterführend Informationen
                </h3>
                <v-row>
                    <v-col>
                        <h5 class="text-h5">Datenvisualisierungen</h5>
                        <v-list>
                            <v-list-item>
                                <v-list-item-icon>
                                    <v-icon color="secondary"
                                        >fa fa-table</v-icon
                                    >
                                </v-list-item-icon>
                                <v-list-item-content>
                                    COVID-Dashboard für Aachen von @rasibo
                                </v-list-item-content>
                            </v-list-item>
                        </v-list>
                    </v-col>
                </v-row>
            </v-card-text> -->
        </v-card>
    </v-container>
</template>

<script>
import Mini from "./charts/Mini.vue";
import Incidence from "./charts/Incidence.vue";
import NewCases from "./charts/NewCases.vue";
import MiniNew from "./charts/MiniNew.vue";

import TrendTable from "./TrendTable.vue";
import OverviewTable from "./OverviewTable.vue";
import HospitalTable from "./HospitalTable.vue";

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
    }),
    methods: {
        ...mapActions({
            updateMuni: "corona/updateMuni",
            load: "corona/load",
        }),
    },
    async mounted() {},
    components: {
        Mini,
        MiniNew,
        Incidence,
        NewCases,
        TrendTable,
        OverviewTable,
        HospitalTable,
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
        ...mapGetters("corona", ["muniName", "muni_data", "todayList"]),
        ...mapState({
            muniDict: (state) => state.corona.muniDict,
            loaded: (state) => state.corona.loaded,
            munis: (state) => state.corona.munis,
            divi: (state) => state.corona.divi,
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
