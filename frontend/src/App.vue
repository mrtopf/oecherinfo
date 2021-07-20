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
            <v-btn icon target="_blank" href="https://twitter.com/oecherinfo">
                <v-icon>fab fa-twitter</v-icon>
            </v-btn>
            <v-tooltip bottom max-width="300" color="rgba(0,0,0,1)">
                <template v-slot:activator="{ on }">
                    <v-btn
                        v-on="on"
                        icon
                        target="_blank"
                        href="https://github.com/mrtopf/oecherinfo"
                    >
                        <v-icon>fab fa-github</v-icon>
                    </v-btn>
                </template>
                Hier findet Du den Source-Code von oecher.info auf github
            </v-tooltip>

            <v-btn
                text
                target="_blank"
                href="https://blog.oecher.info?utm_source=oecher.info&utm_medium=web&utm_campaign=bloglink"
            >
                Blog
            </v-btn>
        </v-app-bar>

        <v-navigation-drawer app v-model="drawer" touchless>
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
                            <v-list-item-title
                                >{{ item.title }}
                            </v-list-item-title>
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
                                        <v-list-item-title
                                            >{{ item.title }}
                                            <v-chip
                                                small
                                                color="#e0e0e"
                                                dark
                                                v-if="item.new"
                                                class="font-weight-bold"
                                            >
                                                <v-icon left size="14">
                                                    fa fa-frown
                                                </v-icon>

                                                alt</v-chip
                                            >
                                        </v-list-item-title>
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
        <v-footer color="primary lighten-1" dark class="footer caption pb-4">
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
export default {
    props: {
        // muni: String
    },
    name: "App",

    computed: {
        muni() {
            const muni = this.$route.params.muni;
            if (!muni) {
                return "sr";
            }
            return muni;
        }
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
            },
            {
                title: "Schnelltests",
                route: "quicktests",
                new: true
            },
            {
                title: "Demographie",
                route: "demographics",
            }
        ]
    }),
    metaInfo: {
        title: "Corona-Dashboard für die Städteregion Aachen",
        titleTemplate: "%s | CORONA | oecher.info",
        meta: [
            {
                name: "description",
                content:
                    "Alle Corona-Daten für die Städteregion Aachen: Inzidenzen, Fallzahlen, Intensivbelegung und deren Entwicklung"
            }
        ]
    }
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
.v-card__text,
.v-card__title {
    word-break: normal !important;
}
.lds-hourglass {
    display: inline-block;
    position: relative;
    width: 80px;
    height: 80px;
}
.lds-hourglass:after {
    content: " ";
    display: block;
    border-radius: 50%;
    width: 0;
    height: 0;
    margin: 8px;
    box-sizing: border-box;
    border: 32px solid #333;
    border-color: #333 transparent #333 transparent;
    animation: lds-hourglass 1.2s infinite;
}
@keyframes lds-hourglass {
    0% {
        transform: rotate(0);
        animation-timing-function: cubic-bezier(0.55, 0.055, 0.675, 0.19);
    }
    50% {
        transform: rotate(900deg);
        animation-timing-function: cubic-bezier(0.215, 0.61, 0.355, 1);
    }
    100% {
        transform: rotate(1800deg);
    }
}
</style>
