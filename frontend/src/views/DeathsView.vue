<template>
    <DataView
        title="Todesfälle"
        :muni="muni"
        :keyAttributes="keyAttributes"
        :attribute="attribute"
    >
        <template v-slot:graphs>
            <CoronaGraph
                class="pb-8 mt-10 mx-0 px-0 mx-md-6"
                title="Todesfälle nach Datum"
                attribute="new_deaths"
                cumulative="deaths"
                :muni="muni"
                :trends="false"
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
    name: "DeathsView",
    data: () => ({
        keyAttributes: [
            {
                name: "heute",
                item: "new_deaths",
                width: 150
            },
            {
                name: "Insgesamt",
                item: "deaths",
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
