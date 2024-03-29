<template>
    <v-card class="ma-0 flex-grow-1 flex-shrink-0" flat color="#f8f8f8">
        <v-card
            flat
            color="transparent"
            v-if="loading"
            class="text-center mt-10 pt-10"
        >
            <div class="lds-hourglass"></div>
        </v-card>

        
        <v-container fluid v-else>

            <v-row no-gutters>
                <v-col cols="12" class="pl-2">
                    <div class="caption black--text mb-6">
                        Zuletzt aktualisiert am {{ date }}
                    </div>
                </v-col>

                <v-col cols="12" md="8" class="pl-2">
                    <MuniSelector
                        v-if="!hideMuniSelector"
                        :title="title"
                        :muni="muni"
                        :attribute="attribute"
                    />
                    <span
                        class="float-left text-h6 text-md-h5 font-weight-bold pl-0 black--text labelButton"
                        v-else
                        >{{ title }}</span
                    >
                </v-col>

                <v-col cols="12" md="4" class="text-md-right d-sm-none d-md-block" v-if="downloadUrl">
                    <v-btn :href="downloadUrl" color="primary" small tile class="my-1">
                        <v-icon small left>fa fa-file-download</v-icon>
                        Daten als CSV herunterladen</v-btn>
                </v-col>
            </v-row>

            <v-divider class="py-3"></v-divider>

            <slot name="info"></slot>

            <v-row v-if="data">
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
                        {{
                            (data.today[attribute.item] || 0).toLocaleString(
                                "de-DE"
                            )
                        }}{{attribute.suffix}}
                    </v-card-text>
                </v-card>
            </v-row>
        </v-container>

        <slot name="graphs" v-if="!loading"></slot>

        <div class="caption text-right py-5 px-2" v-if="!loading">
            Stand {{ date }}<br />
            <span class="l1-line"></span> L1: Lockdown Light, 2.11.2020<br />
            <span class="l2-line"></span> L2: Lockdown 16.12.2020<br />
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
        downloadUrl: String,
        keyAttributes: Array,
        date: String,
        data: Object,
        loading: Boolean,
        hideMuniSelector: Boolean,
    },
    name: "DataView",
    data: () => ({}),
    components: {
        MuniSelector
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
