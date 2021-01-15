<template>
    <DataView
        title="Fallzahlen"
        :muni="muni"
        :keyAttributes="keyAttributes"
        :attribute="attribute"
        :todayData="divi[0]"
    >
        <template v-slot:graphs>
            <CoronaGraph
                class="pb-8 mt-10 mx-0 px-0 mx-md-6"
                title="freie Betten"
                attribute="betten_frei"
                :data="divi_data"
                :barWidth="1"
            />
            <CoronaGraph
                class="pb-8 mt-10 mx-0 px-0 mx-md-6"
                title="COVID-Fälle"
                attribute="covid"
                :data="divi_data"
                :barWidth="1"
            />
            <CoronaGraph
                class="pb-8 mt-10 mx-0 px-0 mx-md-6"
                title="beatmet"
                attribute="ventilated"
                :data="divi_data"
                :barWidth="1"
            />
        </template>
    </DataView>
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";
import DataView from "@/components/DataView.vue";
import CoronaGraph from "@/components/CoronaGraph.vue";
import _ from "lodash"

export default {
    props: {
        muni: {
            type: String,
            default: "sr"
        },
        attribute: String
    },
    name: "CasesView",
    data: () => ({
        keyAttributes: [
            {
                name: "Betten",
                item: "betten_belegt",
                width: 150
            },
            {
                name: "freie Betten",
                item: "betten_frei",
                width: 150
            },
            {
                name: "COVID-Fälle",
                item: "faelle_covid_aktuell",
                width: 150
            },
            {
                name: "davon beatmet",
                item: "faelle_covid_aktuell_beatmet",
                width: 150
            }
        ]
    }),
    computed: {
        divi_data() {
            const revData = _.reverse(this.divi)
            return {
                labels: revData.map( d => d.date),
                betten_frei: revData.map( d => parseInt(d.betten_frei)),
                betten: revData.map( d => parseInt(d.betten)),
                covid: revData.map( d => parseInt(d.faelle_covid_aktuell)),
                ventilated: revData.map( d => parseInt(d.faelle_covid_aktuell_beatmet)),
            }
        },
        ...mapState({
            divi: state => state.corona.divi
        })
    },

    components: {
        DataView,
        CoronaGraph
    }
};
</script>
