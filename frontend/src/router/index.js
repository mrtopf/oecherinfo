import Vue from "vue"
import VueRouter from "vue-router"
import Main from "../views/Main.vue"
import MuniView from "../views/MuniView.vue"
import CasesView from "../views/CasesView.vue"
import RecoveredView from "../views/RecoveredView.vue"
import DeathsView from "../views/DeathsView.vue"

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
    },
    {
        path: "/recovered",
        name: "recovered_sr",
        component: RecoveredView,
        props: true,
    },
    {
        path: "/deaths",
        name: "deaths_sr",
        component: DeathsView,
        props: true,
    },
    {
        path: "/cases/:muni",
        name: "cases",
        component: CasesView,
        props: true,
    },
    {
        path: "/recovered/:muni",
        name: "recovered",
        component: RecoveredView,
        props: true,
    },
    {
        path: "/deaths/:muni",
        name: "deaths",
        component: DeathsView,
        props: true,
    },
    {
        path: "/:muni",
        name: "munidata",
        component: MuniView,
        props: true,
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
    scrollBehavior (to, from, savedPosition) {
        return { x: 0, y: 0 }
    }      
})

export default router
