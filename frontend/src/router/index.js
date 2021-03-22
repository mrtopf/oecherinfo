import Vue from "vue"
import VueRouter from "vue-router"
import Main from "../views/Main.vue"
import CasesView from "../views/CasesView.vue"
import RecoveredView from "../views/RecoveredView.vue"
import DeathsView from "../views/DeathsView.vue"
import HospitalView from "../views/HospitalView.vue"
import DemographicsView from "../views/DemographicsView.vue"
import QuickTests from "../views/QuickTests.vue"

Vue.use(VueRouter)

const routes = [
    {
        path: "/",
        name: "main",
        component: Main,
    },
    {
        path: "/cases",
        name: "cases_sr",
        component: CasesView,
        props: true,
        meta: {
            title: 'oecher.info | Corona Dashboard | Fälle'
        }
    },
    {
        path: "/hospitals",
        name: "hospitals",
        component: HospitalView,
        props: true,
        meta: {
            title: 'oecher.info | Corona Dashboard | Intensivbetten'
        }
    },
    {
        path: "/demographics",
        name: "demographics",
        component: DemographicsView,
        props: true,
        meta: {
            title: 'oecher.info | Corona Dashboard | Demographie'
        }
    },
    {
        path: "/recovered",
        name: "recovered_sr",
        component: RecoveredView,
        props: true,
        meta: {
            title: 'oecher.info | Corona Dashboard | Genesen'
        }
    },
    {
        path: "/deaths",
        name: "deaths_sr",
        component: DeathsView,
        props: true,
        meta: {
            title: 'oecher.info | Corona Dashboard | Todesfälle'
        }
    },
    {
        path: "/cases/:muni",
        name: "cases",
        component: CasesView,
        props: true,
        meta: {
            title: 'oecher.info | Corona Dashboard | Fälle'
        }
    },
    {
        path: "/recovered/:muni",
        name: "recovered",
        component: RecoveredView,
        props: true,
        meta: {
            title: 'oecher.info | Corona Dashboard | Genesen'
        }
    },
    {
        path: "/deaths/:muni",
        name: "deaths",
        component: DeathsView,
        props: true,
        meta: {
            title: 'oecher.info | Corona Dashboard | Todesfälle'
        }
    },
    {
        path: "/quicktests",
        name: "quicktests",
        component: QuickTests,
        props: true,
        meta: {
            title: 'Schnelltests | oecher.info | Corona Dashboard'
        }
    },
    {
        path: "/datenschutz",
        name: "privacy",
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () =>
            import(/* webpackChunkName: "privacy" */ "../views/Datenschutz.vue"),
    },
]

const router = new VueRouter({
    mode: "history",
    base: process.env.BASE_URL,
    routes,
    scrollBehavior(to, from, savedPosition) {
        return { x: 0, y: 0 }
    }
})

export default router
