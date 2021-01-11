import axios from "axios"
import router from "@/router"

const API = process.env.VUE_APP_CORONA_API

const state = {
    loaded: false,
    dateRange: [180, 190],
    dateRangeName: "1month",
    data: {},
    date: null,
    allMuniData: {},
    muniDict: {},
    divi: {},
    hospitals: {},
    today: {},
    yesterday: {},
    weekerday: {},
    yesterdate: null,
    selectedMuni: "aachen",
    munis: [], // list of all known munis in select style
}

const getters = {
    muni_data: (state) => {
        const routerMuni = router.currentRoute.params.muni
        if (routerMuni) {
            return state.allMuniData[routerMuni]
        }
        const data = state.allMuniData[state.selectedMuni]
        return data
    },
    muniName: (state) => {
        let selected = state.selectedMuni
        const routerMuni = router.currentRoute.params.muni
        if (routerMuni) {
            selected = routerMuni
        }
        if (selected == "sr") {
            return "Städteregion Aachen"
        } else {
            return state.muniDict[selected]
        }
    },
    // return the list for today
    todayList: (state) => {
        // return today as list
        let res = []
        for (const muni in state.today) {
            const tData = state.today[muni]
            const yData = state.yesterday[muni]
            const wData = state.weekerday[muni]
            let rec = {
                municipality_name: tData["municipality_name"],
                muni: tData["municipality"],
            }
            if (muni == "sr") {
                rec["rowClass"] = "totalRow"
                rec["municipality_name"] = "Gesamtergebnis"
            }
            for (const prop of [
                "new",
                "active",
                "incidence",
                "deaths",
                "recovered",
                "positive",
                "new_avg",
                "active_avg",
                "incidence_avg",
                "deaths_avg",
                "recovered_avg",
                "positive_avg",
            ]) {
                rec[prop] = Math.round(tData[prop])
                rec[prop + "_diff"] = Math.round(tData[prop] - yData[prop])

                // compute trends via data from week ago
                const d = Math.round(tData[prop] - wData[prop])
                if (d > 0) {
                    rec[prop + "_trend_color"] = "red"
                    rec[prop + "_trend_icon"] = "fas fa-chevron-up"
                } else if (d < 0) {
                    rec[prop + "_trend_color"] = "green"
                    rec[prop + "_trend_icon"] = "fas fa-chevron-down"
                } else {
                    rec[prop + "_trend_color"] = "grey"
                    rec[prop + "_trend_icon"] = "fa fa-minus"
                }
            }
            res.push(rec)
        }
        return res
    },
}

const actions = {
    async load({ commit, dispatch }) {
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
                commit("storeDIVIData", response.data.divi)
                commit("storeHospitals", response.data.hospitals)
                commit("setLoaded")
            })
            .catch((error) => {
                console.log(error)
                alert("Ein Fehler ist beim Laden der Daten aufgetreten")
            })
    },
    updateMuni({ commit }, muni) {
        commit("setMuni", muni)
    },
    setDateRangeStart({commit, state, getters}, dateRangeName) {
        commit("setDateRangeName", dateRangeName)
        const end = getters.muni_data.incidence.length;
        if (dateRangeName == "w2") {
            commit("setDateRange", [state.selectedMuni == "sr" ? 180 : 54, end])
        } else if (dateRangeName == "1month") {
            commit("setDateRange", [end-31, end])
        } else if (dateRangeName == "all") {
            commit("setDateRange", [0, end])
        } else {
            commit("setDateRange", [0, end])
        }
    }
}
const mutations = {
    storeMunis(state, munis) {
        state.muniDict = munis
        let allMunis = []
        for (const muni in munis) {
            if (muni == "sr") {
                allMunis.unshift({
                    muni: muni,
                    name: "Städteregion Aachen",
                })
            } else {
                allMunis.push({
                    muni: muni,
                    name: munis[muni],
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
    storeDIVIData(state, data) {
        state.divi = data
    },
    storeHospitals(state, data) {
        state.hospitals = data
    },
    setMuni(state, muni) {
        state.selectedMuni = muni
    },
    setLoaded(state) {
        state.loaded = true
    },
    setLoading(state) {
        state.loaded = false
    },
    setDateRange(state, range) {
        state.dateRange = range
    },
    setDateRangeName(state, dateRangeName) {
        state.dateRangeName = dateRangeName
    },
}

export const corona = {
    namespaced: true,
    state,
    getters,
    actions,
    mutations,
}
