<template>
    <DataView
        title="Fallzahlen"
        :muni="muni"
        :keyAttributes="keyAttributes"
        :attribute="attribute"
        :todayData="today[muni]"
    >
        <template v-slot:graphs>
            <CoronaGraph
                class="pb-8 mt-10 mx-0 px-0 mx-md-6"
                title="7-Tage-Inzidenz"
                attribute="incidence"
                :data="muni_data"
            />
            <CoronaGraph
                class="pb-8 mt-10 mx-0 px-0 mx-md-6"
                title="Neue Fälle nach Datum"
                attribute="new"
                cumulative="positive"
                :data="muni_data"
            />
            <CoronaGraph
                class="pb-8 mt-10 mx-0 px-0 mx-md-6"
                title="Aktive Fälle"
                attribute="active"
                :data="muni_data"
            />
        </template>
    </DataView>
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";
import DataView from "@/components/DataView.vue";
import CoronaGraph from "@/components/CoronaGraph.vue";

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
            }
        ]
    }),

    computed: {
        muni_data() {
            return this.allMuniData[this.muni];
        },
        ...mapState({
            allMuniData: state => state.corona.allMuniData,
            today: state => state.corona.today
        })
    },

    components: {
        DataView,
        CoronaGraph
    }
};
</script>
