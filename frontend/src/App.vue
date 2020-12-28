<template>
    <v-app>
        <v-app-bar :dense="$vuetify.breakpoint.mobile" app color="primary" dark>
            <v-app-bar-nav-icon
                @click.stop="drawer = !drawer"
            ></v-app-bar-nav-icon>
            <v-toolbar-title dark class="pa-0">
                <v-btn
                    text
                    class="text-xs-caption text-lg-h5"
                    exact
                    @click="$router.push('/')"
                >
                    <span class="font-weight-bold"> oecher.info </span>
                    <span class="font-weight-thin"> | corona </span>
                </v-btn>
            </v-toolbar-title>
            <v-spacer></v-spacer>
        </v-app-bar>

                
        <v-navigation-drawer temporary absolute v-model="drawer">
            <v-list-item>
                <v-list-item-content>
                    <v-list-item-icon>
                        <v-icon>fa fa-virus</v-icon>
                    </v-list-item-icon>
                    <v-list-item-title class="title">
                        Corona-Daten
                    </v-list-item-title>
                </v-list-item-content>
            </v-list-item>
            <v-divider></v-divider>
            <v-list dense nav>
                <v-list-item key="dash" link to="/">
                    <v-list-item-content>
                        <v-list-item-title class="font-weight-bold"
                            >Übersicht</v-list-item-title
                        >
                    </v-list-item-content>
                </v-list-item>
                <v-list-item
                    v-for="item in $store.state.corona.munis"
                    :key="item.value"
                    link
                    :to="{
                        name: 'munidata',
                        params: { attribute: 'incidence', muni: item.muni },
                    }"
                >
                    <v-list-item-content>
                        <v-list-item-title>{{ item.name }}</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
            </v-list>
        </v-navigation-drawer>

        <v-main>
            <!-- {{$vuetify.breakpoint.name}} -->
            <router-view></router-view>
        </v-main>
        <v-footer color="primary lighten-1" dark class="footer caption">
            <v-row dense>
                <v-col cols="12" lg=6>
                    Ein Projekt von
                    <a target="_blank" href="https://twitter.com/mrtopf"
                        >Christian "MrTopf" Scholz</a
                    >
                </v-col>

                <v-col class="text-md-right" cols="12" lg=6>
                    <a href="/datenschutz">Datenschutz</a> |
                    <a target="_blank" href="https://mrtopf.de/impressum"
                        >IMPRESSUM</a
                    >
                </v-col>
            </v-row>
        </v-footer>
    </v-app>
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";

export default {
    props: {
        muni: String,
    },
    name: "App",

    mounted() {
        this.loadCoronaData();
    },

    methods: {
        ...mapActions({
            loadCoronaData: "corona/load",
            updateMuni: "corona/updateMuni",
        }),
    },
    computed: {
        ...mapGetters("corona", ["muni_data"]),
        ...mapState({
            munis: (state) => state.corona.munis,
            today: (state) => state.corona.today,
            loaded: (state) => state.corona.loaded,
            date: (state) => state.corona.date,
            selectedMuni: (state) => state.corona.selectedMuni,
        }),
    },
    data: () => ({
        mymuni: "sr",
        drawer: false,
    }),
};
</script>
<style lang="scss">
.footer a {
    color: white !important;
}
</style>
