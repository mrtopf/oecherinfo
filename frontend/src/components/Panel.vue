<template>
    <v-card color="#fff" class="ma-3 pa-3" tile>
        <v-card-title
            primary-title
            class="text-h6 text-md-h4 font-weight-bold primary--text"
        >
            {{ title }}
        </v-card-title>
        <v-card-text style="max-width: 1024px;" class="body-2 pr-10 pl-5">
            <slot name="description"></slot>
        </v-card-text>
        <v-card-text>
            <v-tabs
                ref="tabs"
                v-model="view"
                background-color="#fff"
                class="graph-tabs"
                active-class="graph-tab-active"
            >
                <v-tab
                    v-for="tab in allTabs"
                    :key="tab.id"
                    class="body-2 font-weight-bold"
                    @click="
                        $matomo &&
                            $matomo.trackEvent(
                                'Corona',
                                'graphclick-' + tab.id,
                                matomoAttribute
                            )
                    "
                >
                    {{ tab.title }}
                </v-tab>
            </v-tabs>
            <v-tabs-items v-model="view">
                <v-tab-item transition="none" v-for="tab in tabs" :key="tab.id">
                    <slot :name="`tab.${tab.id}`"></slot>
                </v-tab-item>

                <v-tab-item transition="none" key="data">
                    <v-card flat color="#fff">
                        <v-data-table
                            fixed-header
                            id="data-table"
                            must-sort
                            sort-by="date"
                            sort-desc
                            dense
                            disable-pagination
                            hide-default-footer
                            :headers="tableHeaders"
                            :items="tableData"
                            :height="$vuetify.breakpoint.mdAndUp ? 500 : 280"
                        >
                            <template v-slot:item.dates="item">
                                {{ item.item.dates | moment("D.M.Y") }}
                            </template>
                        </v-data-table>
                    </v-card>
                </v-tab-item>
            </v-tabs-items>
        </v-card-text>
    </v-card>
</template>

<script>
import { map } from "lodash";

export default {
    props: {
        tabs: Array,
        matomoAttribute: String, // used for matomo to know which graph was clicked on
        title: String,
        tableAttributes: Array,
        data: Object,
    },
    data() {
        return {
            view: 0
        };
    },
    computed: {
        allTabs() {
            return [...this.tabs, { id: "data", title: "Daten" }];
        },
        tableHeaders() {
            let headers = [
                {
                    text: "Datum",
                    value: "dates",
                    sortable: true,
                    sort: (a, b) => (new Date(a) < new Date(b) ? -1 : 1)
                }
            ]
            for (const h of this.tableAttributes) {
                headers.push({
                    text: h.text,
                    value: h.value,
                    sortable: true
                })
            }
            return headers;
        },
        tableData() {
            const selectedAttributes = [...map(this.tableAttributes, "value"), 'dates']
            
            // construct [{key: value},...] from {'key': [value, ...], ...} in this.data
            let data = [];
            for (const idx in this.data['dates']) {
                let record = {}
                for (const attr of selectedAttributes) {
                    record[attr] = this.data[attr][idx]
                }
                data.push(record)
            }
            return data
        }
    }
};
</script>