<template>
    <DataView
        title="Fallzahlen"
        :muni="muni"
        :keyAttributes="keyAttributes"
        :attribute="attribute"
    >
        <template v-slot:graphs>
            <CoronaGraph
                class="pb-8 mt-10 mx-0 px-0 mx-md-6"
                title="7-Tage-Inzidenz"
                attribute="incidence"
                :muni="muni"
            />
            <CoronaGraph
                class="pb-8 mt-10 mx-0 px-0 mx-md-6"
                title="Neue Fälle nach Datum"
                attribute="new"
                cumulative="positive"
                :muni="muni"
            />
            <CoronaGraph
                class="pb-8 mt-10 mx-0 px-0 mx-md-6"
                title="Aktive Fälle"
                attribute="active"
                :muni="muni"
            />
        </template>
    </DataView>
</template>

<script>
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

    components: {
        DataView,
        CoronaGraph
    }
};
</script>
