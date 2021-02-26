import Vue from "vue"
import "./plugins/axios"
import App from "./App.vue"
import router from "./router"
import store from "./store"
import vuetify from "./plugins/vuetify"

import ECharts from 'vue-echarts'

import * as echarts from "echarts/core";
const { use, registerMap, registerTheme } = echarts;

import { CanvasRenderer } from "echarts/renderers";
import { BarChart, LineChart } from "echarts/charts";
import {
    DataZoomComponent,
    VisualMapComponent,
    MarkLineComponent,
    DataZoomSliderComponent, 
    GridComponent, 
    TooltipComponent,
    ToolboxComponent,
} from "echarts/components";

use([BarChart, 
    VisualMapComponent,
    GridComponent, 
    TooltipComponent, 
    LineChart, 
    DataZoomComponent,
    DataZoomSliderComponent, 
    MarkLineComponent,
    ToolboxComponent,
    CanvasRenderer]);


// register globally (or you can do it locally)
Vue.component('v-chart', ECharts)


import VueMoment from 'vue-moment'
Vue.use(VueMoment, {
})

const MATOMO_URL = process.env.VUE_APP_MATOMO_URL
const MATOMO_ID = process.env.VUE_APP_MATOMO_ID
const MATOMO_DOMAINS = process.env.MATOMO_DOMAINS

import VueMatomo from 'vue-matomo'

Vue.use(VueMatomo, {
    // Configure your matomo server and site by providing
    host: MATOMO_URL,
    siteId: MATOMO_ID,

    router: router,
    enableLinkTracking: true,
    disableCookies: true,
    debug: false,

    // Tell Matomo the website domain so that clicks on these domains are not tracked as 'Outlinks'
    // Default: undefined, example: '*.example.com'
    domains: MATOMO_DOMAINS, // 'oecher.info'
});


Vue.config.productionTip = false

new Vue({
    router,
    store,
    vuetify,
    render: (h) => h(App),
}).$mount("#app")
