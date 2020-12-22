import axios from "axios";
import router from '@/router'


const API = process.env.VUE_APP_CORONA_API;

const state = {
    loaded: false,
    data: {},
    date: null,
    allMuniData: {},
    muniDict: {},
    today: {},
    yesterday: {},
    weekerday: {},
    yesterdate: null,
    selectedMuni: "aachen",
    munis: [], // list of all known munis in select style
}

const getters = {
    muni_data: state => {
        const routerMuni = router.currentRoute.params.muni
        if (routerMuni) {
            return state.allMuniData[routerMuni]
        }
        const data = state.allMuniData[state.selectedMuni]
        return data
    },
    muniName: state => {
        let selected = state.selectedMuni
        const routerMuni = router.currentRoute.params.muni
        if (routerMuni) {
            selected = routerMuni
        }
        if (selected== "sr") {
            return "Städteregion Aachen";
        } else {
            return state.muniDict[selected];
        }
    },
}

const actions = {
    async load({commit, dispatch}) {
        commit("setLoading")
        axios
            .get(`${API}/all`)
            .then((response) => {
                commit("storeMunis", response.data.munis)
                commit("storeToday", response.data.today)
                commit("storeYesterday", response.data.yesterday)
                commit("storeWeekerday", response.data.weekerday)
                commit("storeYesterdate", response.data.yesterdateFormatted)
                commit("storeDate", response.data.dateFormatted)
                commit("storeMuniData", response.data.muni_data)
                commit("setLoaded")
            })
            .catch((error) => {
                console.log(error)
                alert("Ein Fehler ist beim Laden der Daten aufgetreten")
            })
    },
    updateMuni({commit, state}, muni) {
        commit("setMuni", muni.muni)
    }
}
const mutations = {
    storeMunis(state, munis) {
        state.muniDict = munis
        let allMunis = []
        for (const muni in munis) {
            if (muni=="sr") {
                allMunis.unshift({
                    muni: muni,
                    name: "Städteregion Aachen"
                })
            } else {
                allMunis.push({
                    muni: muni,
                    name: munis[muni]
                })
            }
        }
        state.munis = allMunis
    },
    storeToday(state, data) {
        state.today = data
    },
    storeYesterday(state, data) {
        state.yesterday = data
    },
    storeWeekerday(state, data) {
        state.weekerday = data
    },
    storeDate(state, date) {
        state.date = date
    },
    storeYesterdate(state, date) {
        state.yesterdate = date
    },
    storeMuniData(state, data) {
        state.allMuniData = data
    },
    setMuni(state, muni) {
        Object.keys(state.muniDict).indexOf(muni)
        state.selectedMuni = muni
    },
    setLoaded(state) {
        state.loaded = true
    },
    setLoading(state) {
        state.loaded = false
    }
}

export const corona = {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}