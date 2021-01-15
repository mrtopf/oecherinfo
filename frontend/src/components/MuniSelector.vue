<template>
    <v-toolbar-title class="font-weight-bold text-uppercase">
        <v-menu offset-y bottom left>
            <template v-slot:activator="{ on }">
                <v-btn
                    text
                    class="float-left text-h6 text-md-h5 font-weight-bold pl-0 black--text labelButton"
                    disabled
                >{{ title }}
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
                    v-for="item in $store.state.corona.munis"
                    :key="item.value"
                    link
                    :to="{
                        name: $route.name,
                        params: {
                            attribute: attribute,
                            muni: item.muni
                        }
                    }"
                >
                    <v-list-item-content>
                        <v-list-item-title>{{ item.name }}</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
            </v-list>
        </v-menu>
    </v-toolbar-title>
</template>
<script>
import { mapState, mapActions, mapGetters } from "vuex";

export default {
    props: {
        title: String,
        attribute: String,
        muni: {
            type: String,
            default: "sr"
        }
    },
    computed: {
        ...mapState({
            muniDict: state => state.corona.muniDict
        })
    }
};
</script>
<style scoped>
.labelButton {
    padding-right: 10px !important;
}
.labelButton >>> .v-btn__content {
    color: #023047 !important;
    padding-left: 0 !important;
    margin-left: 0 !important;
    position: relative;
    left: -2px;
}
</style>