<template>
    <v-card tile flat elevation="4">
        <v-data-table
            :headers="headers"
            :items="todayList"
            item-key="municipality"
            :items-per-page="20"
            item-class="rowClass"
            hide-default-footer
            :custom-sort="sortTable"
            id="corona-table"
            @click:row="handleMuniClick"
        >
            <template v-slot:item.active="{ item }">
                {{ item.active }}
                <small v-if="item.active_diff < 0">
                    ({{ item.active_diff }})
                </small>
                <small v-if="item.active_diff > 0">
                    (-{{ item.active_diff }})
                </small>
            </template>
            <template v-slot:item.recovered="{ item }">
                {{ item.recovered }}
                <small v-if="item.recovered_diff < 0">
                    ({{ item.recovered_diff }})
                </small>
                <small v-if="item.recovered_diff > 0">
                    (+{{ item.recovered_diff }})
                </small>
            </template>
            <template v-slot:item.incidence="{ item }">
                <v-chip
                    :color="getChipColor(item.incidence)"
                    :dark="item.incidence > 200"
                >
                    {{ item.incidence }}
                    <small v-if="item.incidence_diff > 0">
                        (+{{ item.incidence_diff }})
                    </small>
                    <small v-if="item.incidence_diff < 0">
                        ({{ item.incidence_diff }})
                    </small>
                </v-chip>
            </template>
        </v-data-table>
    </v-card>
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";
export default {
    props: {
        selectedMuni: String,
    },
    methods: {
        sortTable(items, sortBy, sortDesc) {
            // this mainly keeps the SR element on bottom
            const parts = _.partition(items, (o) => o.muni == "sr"); // split into sr or not
            const d = sortDesc[0] ? "desc" : "asc";
            let result = _.orderBy(parts[1], [sortBy], [d]);
            result.push(parts[0][0]);
            return result;
        },
        handleMuniClick(item) {
            this.$router.push({
                name: "munidata",
                params: {
                    attribute: "incidence",
                    muni: item.muni,
                },
            });
        },
        getChipColor(incidence) {
            if (incidence > 200) {
                return "#EF476F";
            } else if (incidence > 50) {
                return "#FFC43D";
            }
            return "#7FEBC3";
        },
    },
    computed: {
        todayListFiltered() {
            return _.filter(
                this.todayList,
                (item) => item.muni == "sr" || item.muni == this.selectedMuni
            );
        },
        ...mapGetters("corona", ["muniName", "muni_data", "todayList"]),
    },
    data() {
        return {
            headers: [
                {
                    text: "Kommune",
                    align: "start",
                    sortable: true,
                    value: "municipality_name",
                },
                { text: "Aktiv", value: "active" },
                { text: "Neue Fälle", value: "new" },
                { text: "Fälle insgesamt", value: "positive" },
                { text: "Genesen", value: "recovered" },
                { text: "Verstorben", value: "deaths" },
                { text: "Inzidenz", value: "incidence" },
            ],
        };
    },
};
</script>
<style lang="scss">
.totalRow {
    background: #2f2f2f;
    color: white;
    font-weight: bold;
    td {
        background: #2f2f2f;
    }
}
#corona-table {
    tr {
        cursor: pointer;
    }
}
#corona-table .v-data-table-header tr {
    th {
        font-weight: bold;
        color: black;
        font-size: 14px !important;
    }
}
</style>