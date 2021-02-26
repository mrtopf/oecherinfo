<template>
    <v-card
        class="ma-0 flex-grow-1 flex-shrink-0"
        flat
        color="#f8f8f8"
    >
        <v-container fluid>
            <v-row no-gutters>
                <v-col cols="12" class="pl-2">
                    <div class="caption black--text mb-6">
                        Zuletzt aktualisiert am {{ date }}
                    </div>
                </v-col>
                <v-col cols="12" md="8" class="pl-2">
                    <MuniSelector
                        :title="title"
                        :muni="muni"
                        :attribute="attribute"
                    />
                </v-col>
            </v-row>

            <v-divider></v-divider>
            <v-row>
                <v-card
                    flat
                    class="mx-2 pb-0"
                    :width="attribute.width"
                    :key="attribute.name"
                    color="#f8f8f8"
                    v-for="attribute in keyAttributes"
                >
                    <v-card-text class="font-weight-bold caption pb-0 mt-0">
                        {{ attribute.name }}
                    </v-card-text>
                    <v-card-text
                        class="font-weight-bold text-h4 mt-0 pt-0 pb-0 mb-0"
                    >
                        {{ (todayData[attribute.item] || 0).toLocaleString("de-DE")  }}
                    </v-card-text>
                </v-card>
            </v-row>
        </v-container>

        <slot name="graphs"></slot>

        <div class="caption text-right py-5 px-2">
            Stand {{ date }}<br />
            <span class="l1-line"></span> Lockdown Light, 2.11.2020<br />
            <span class="l2-line"></span> Lockdown 16.12.2020<br />
        </div>
    </v-card>
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";

import MuniSelector from "@/components/MuniSelector.vue";

export default {
    props: {
        title: String,
        muni: {
            type: String,
            default: "sr"
        },
        attribute: String,
        keyAttributes: Array,
        todayData: Object,
        date: String,
    },
    name: "DataView",
    data: () => ({
    }),
    components: {
        MuniSelector
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
