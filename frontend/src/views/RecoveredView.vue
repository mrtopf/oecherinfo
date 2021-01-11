<template>
    <DataView
        title="Genesene"
        :muni="muni"
        :keyAttributes="keyAttributes"
        :attribute="attribute"
    >
        <template v-slot:graphs>
            <CoronaGraph
                class="pb-8 mt-10 mx-0 px-0 mx-md-6"
                title="Genesene nach Datum"
                attribute="new_recovered"
                cumulative="recovered"
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
    name: "RecoveredView",
    data: () => ({
        keyAttributes: [
            {
                name: "heute",
                item: "new_recovered",
                width: 150
            },
            {
                name: "Insgesamt",
                item: "recovered",
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
