<template>
    <v-app>
        <v-app-bar :dense="$vuetify.breakpoint.mobile" app color="primary" dark>
            <v-app-bar-nav-icon
                @click.stop="drawer = !drawer"
            ></v-app-bar-nav-icon>
            <v-toolbar-title dark class="pa-0">
                <v-btn
                    text
                    class="text-xs-caption text-md-h5"
                    exact
                    @click="$router.push('/').catch(() => {})"
                >
                    <span class="font-weight-bold"> oecher.info </span>
                    <span class="font-weight-thin"> | corona </span>
                </v-btn>
            </v-toolbar-title>
            <v-spacer></v-spacer>
            <v-btn
                text
                href="https://blog.oecher.info?utm_source=oecher.info&utm_medium=web&utm_campaign=bloglink"
            >
                Blog
            </v-btn>
        </v-app-bar>

        <v-navigation-drawer temporary absolute v-model="drawer">
            <v-list-item>
                <v-list-item-content>
                    <v-list-item-title class="title">
                        Corona-Daten
                    </v-list-item-title>
                </v-list-item-content>
            </v-list-item>
            <v-divider></v-divider>
            <v-list nav class="" id="2av-list">
                <v-list-item-group
                    v-model="activeTab"
                    active-class="nav-active"
                >
                    <v-list-item
                        :ripple="false"
                        v-for="item in navItems"
                        :key="item.title"
                        :to="{
                            name: item.route,
                            params: {
                                muni: muni
                            }
                        }"
                        link
                        exact
                        :active="item.active"
                    >
                        <v-list-item-content>
                            <v-list-item-title>{{
                                item.title
                            }}</v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                </v-list-item-group>
            </v-list>
        </v-navigation-drawer>

        <v-main>
            <v-container fluid class="pa-0">
                <v-row no-gutters>
                    <v-col cols="12" md="2" class="d-none d-md-flex">
                        <v-list
                            nav
                            class="mt-4 pl-7"
                            id="nav-list"
                            color="#f8f8f8"
                        >
                            <v-list-item-group
                                v-model="activeTab"
                                active-class="nav-active"
                            >
                                <v-list-item
                                    :ripple="false"
                                    v-for="(item, i) in navItems"
                                    :key="item.title"
                                    :to="{
                                        name: item.route,
                                        params: {
                                            muni: muni
                                        }
                                    }"
                                    :nexact="muni != 'sr' || i == 0"
                                    link
                                    :exact="i == 0"
                                    :active="item.active"
                                >
                                    <v-list-item-content>
                                        <v-list-item-title>{{
                                            item.title
                                        }}</v-list-item-title>
                                    </v-list-item-content>
                                </v-list-item>
                            </v-list-item-group>
                        </v-list>
                    </v-col>
                    <v-col cols="12" md="10">
                        <router-view></router-view>
                    </v-col>
                </v-row>
            </v-container>
        </v-main>
        <v-footer color="primary lighten-1" dark class="footer caption">
            <v-row dense>
                <v-col cols="12" lg="6">
                    Ein Projekt von
                    <a target="_blank" href="https://twitter.com/mrtopf"
                        >Christian "MrTopf" Scholz</a
                    >
                </v-col>

                <v-col class="text-md-right" cols="12" lg="6">
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
        // muni: String
    },
    name: "App",

    mounted() {
        this.loadCoronaData();
    },

    methods: {
        ...mapActions({
            loadCoronaData: "corona/load",
            updateMuni: "corona/updateMuni"
        })
    },
    computed: {
        muni() {
            const muni = this.$route.params.muni;
            if (!muni) {
                return "sr";
            }
            return muni;
        },
        ...mapGetters("corona", ["muni_data"]),
        ...mapState({
            munis: state => state.corona.munis,
            today: state => state.corona.today,
            loaded: state => state.corona.loaded,
            date: state => state.corona.date,
            selectedMuni: state => state.corona.selectedMuni
        })
    },
    watch: {
        $route(to, from) {
            document.title = to.meta.title || "oecher.info | Corona Dashboard";
        }
    },

    data: () => ({
        mymuni: "sr",
        drawer: false,
        activeTab: 0,
        navItems: [
            {
                title: "Übersicht",
                route: "main"
            },
            {
                title: "Fallzahlen",
                active: true,
                route: "cases"
            },
            {
                title: "Genesen",
                route: "recovered"
            },
            {
                title: "Todesfälle",
                route: "deaths"
            },
            {
                title: "Intensivbetten",
                route: "hospitals"
            }
        ]
    })
};
</script>
<style >
main {
    background: #f8f8f8;
}
.footer a {
    color: white !important;
}
.ttip {
    border-bottom: 1px dashed rgba(0, 0, 0, 0.5);
    cursor: pointer;
}
.nav-active:before {
    border-radius: 0 !important;
    opacity: 0;
}

.nav-active {
    border-radius: 0 !important;
    background: #158897;
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
