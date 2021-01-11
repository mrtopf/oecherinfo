<template>
    <v-card v-if="muni_data" class="ma-0 flex-grow-1 flex-shrink-0" flat>
        <v-container fluid>
            <v-row no-gutters>
                <v-col cols="12" class="pl-2">
                    <div class="caption black--text mb-6">
                        Zuletzt aktualisiert am {{ date }}
                    </div>
                </v-col>
                <v-col cols="12" md="8" class="pl-2">
                    <MuniSelector :title="title" :muni="muni" />
                </v-col>
                <v-col cols="12" md="4" class="text-md-right pl-0">
                    <v-menu offset-y bottom left>
                        <template v-slot:activator="{ on }">
                            <v-btn
                                color="primary"
                                dark
                                text
                                class="pl-2"
                                v-on="on"
                            >
                                Zeitspanne:
                                {{ dateRangeTitles[dateRangeName] }}
                                <v-icon right>fa fa-caret-down</v-icon>
                            </v-btn>
                        </template>
                        <v-list>
                            <v-list-item
                                class="font-weight-bold text-uppercase"
                            >
                                <v-icon small left>fa fa-calendar-alt</v-icon>

                                Zeitfenster
                            </v-list-item>
                            <v-divider></v-divider>
                            <v-list-item
                                @click="
                                    setDateRangeStart('all');
                                    $matomo.trackEvent(
                                        'Corona',
                                        'change-daterange',
                                        'all'
                                    );
                                "
                                >komplett</v-list-item
                            >
                            <v-list-item
                                @click="
                                    setDateRangeStart('w2');
                                    $matomo.trackEvent(
                                        'Corona',
                                        'change-daterange',
                                        'w2'
                                    );
                                "
                                >2. Welle</v-list-item
                            >
                            <v-list-item
                                @click="
                                    setDateRangeStart('1month');
                                    $matomo.trackEvent(
                                        'Corona',
                                        'change-daterange',
                                        '1month'
                                    );
                                "
                                >letzter Monat</v-list-item
                            >
                        </v-list>
                    </v-menu>
                </v-col>
            </v-row>
        </v-container>

        <v-divider></v-divider>
        <v-row>
            <v-card
                flat
                class="mx-6 pb-0"
                :width="attribute.width"
                :key="attribute.name"
                v-for="attribute in keyAttributes"
            >
                <v-card-text class="font-weight-bold caption pb-0 mt-0">
                    {{ attribute.name }}
                </v-card-text>
                <v-card-text
                    class="font-weight-bold text-h3 mt-0 pt-0 pb-0 mb-0"
                >
                    {{ Math.round(today[muni][attribute.item]) }}
                </v-card-text>
            </v-card>
        </v-row>
        <slot name="graphs">hi, graphs here!</slot>

        <div class="caption text-right py-5 px-2">
            Stand {{ date }}<br />
            <span class="l1-line"></span> Lockdown Light, 2.11.2020<br />
            <span class="l2-line"></span> Weihnachts-Lockdown, 16.12.2020
        </div>
    </v-card>
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";

import CoronaGraph from "@/components/CoronaGraph.vue";
import MuniSelector from "@/components/MuniSelector.vue";

export default {
    props: {
        title: String,
        muni: {
            type: String,
            default: "sr"
        },
        attribute: String,
        keyAttributes: Array
    },
    name: "DataView",
    data: () => ({
        dateRangeTitles: {
            all: "alles",
            w2: "ab 2. Welle",
            "1month": "letzter Monat"
        }
    }),
    mounted() {
        if (this.muni_data) {
            this.setDateRangeStart("all");
        }
        this.updateMuni(this.muni);
    },
    watch: {
        muni_data(val, oldval) {
            this.setDateRangeStart("all");
        }
    },
    methods: {
        ...mapActions({
            setDateRangeStart: "corona/setDateRangeStart",
            updateMuni: "corona/updateMuni"
        })
    },
    components: {
        CoronaGraph,
        MuniSelector
    },
    computed: {
        muni_data() {
            return this.allMuniData[this.muni];
        },
        ...mapGetters("corona", ["muniName"]),
        ...mapState({
            muniDict: state => state.corona.muniDict,
            loaded: state => state.corona.loaded,
            munis: state => state.corona.munis,
            allMuniData: state => state.corona.allMuniData,
            today: state => state.corona.today,
            yesterday: state => state.corona.yesterday,
            weekerday: state => state.corona.weekerday,
            date: state => state.corona.date,
            dateRange: state => state.corona.dateRange,
            dateRangeName: state => state.corona.dateRangeName
        })
    }
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
.nav-active:before {
    border-radius: 0 !important;
    opacity: 0;
}
.nav-active {
    border-radius: 0;
    background: #1b9aaa;
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
