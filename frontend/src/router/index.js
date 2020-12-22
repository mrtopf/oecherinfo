import Vue from "vue"
import VueRouter from "vue-router"
import Main from "../views/Main.vue"
//import IncidenceView from "../views/IncidenceView.vue"
import MuniView from "../views/MuniView.vue"
import CoronaGraph from "../components/CoronaGraph.vue"

Vue.use(VueRouter)

const routes = [
    {
        path: "/",
        name: "Main",
        component: Main,
    },
    {
        path: "/:muni",
        name: "munidata",
        component: MuniView,
        props: true,
        // children: [
        //     {
        //         name: "incidence",
        //         path: ":attribute",
        //         component: CoronaGraph,
        //         props: true,
        //     },
        //     {
        //         name: "active",
        //         path: ":attribute",
        //         component: CoronaGraph,
        //         props: true,
        //     },
        // ]
    },
    // {
    //     path: "/:muni/:attribute",
    //     name: "munigraph",
    //     component: CoronaGraph,
    //     props: true,
    // },
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
})

export default router
