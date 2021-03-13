<template>
    <v-card color="#fff" class="pb-8 mt-10 mx-0 px-0 mx-md-6" tile>
        <v-card-title
            primary-title
            class="text-h6 text-md-h4 font-weight-bold primary--text"
        >
            {{ title }}: <span class="pl-2">{{ todayValue || 0 }}</span>
            <v-tooltip bottom max-width="300" v-if="showTrends">
                <template v-slot:activator="{ on }">
                    <span v-on="on" class="ml-3 mr-3 pa-0 ttip">
                        <small class="text-h6 text-md-h6 caption"
                            >{{ diffYesterday }}
                        </small>
                    </span>
                </template>
                Unterschied zum Vortag
            </v-tooltip>
            <v-tooltip bottom max-width="300" v-if="showTrends">
                <template v-slot:activator="{ on }">
                    <span class="ttip">
                        <v-icon
                            v-on="on"
                            :color="trend.color"
                            :size="$vuetify.breakpoint.smAndUp ? 30 : 20"
                            :style="trend.rotate"
                            class="pa-0 pl-1 pr-5 ma-0 trend-icon"
                            >{{ trend.icon }}</v-icon
                        >
                    </span>
                </template>
                <span
                    >Der Langzeittrend ist die Differenz des Wertes von vor 7
                    Tagen verglichen mit dem aktuellen Wert.</span
                >
            </v-tooltip>
        </v-card-title>
        <v-card-text style="max-width: 1024px;" class="body-2 pr-10 pl-5">
            <slot name="description"></slot>
        </v-card-text>
        <v-card-text :class="$vuetify.breakpoint.mdAndUp ? '' : 'px-0'">
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
            <v-tabs-items v-model="view" touchless>
                <v-tab-item transition="none" v-for="tab in tabs" :key="tab.id" :class="$vuetify.breakpoint.mdAndUp ? '' : 'py-4 pa-0'">
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
                                {{ item.item.dates | dateformat }}
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
        attribute: String, // attribute to use for header numbers
        showTrends: {
            type: Boolean,
            default: true
        }
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
            ];
            for (const h of this.tableAttributes) {
                headers.push({
                    text: h.text,
                    value: h.value,
                    sortable: true
                });
            }
            return headers;
        },
        tableData() {
            const selectedAttributes = [
                ...map(this.tableAttributes, "value"),
                "dates"
            ];

            // construct [{key: value},...] from {'key': [value, ...], ...} in this.data
            let data = [];
            for (const idx in this.data["dates"]) {
                let record = {};
                for (const attr of selectedAttributes) {
                    record[attr] = this.data[attr][idx];
                }
                data.push(record);
            }
            return data;
        },
        todayValue() {
            return this.data.today[this.attribute];
        },
        diffYesterday() {
            const d = Math.round(
                this.data.today[this.attribute] -
                    this.data.yesterday[this.attribute],
                2
            );
            if (d > 0) {
                return "+" + d;
            } else if (d < 0) {
                return d;
            } else {
                return "+/- 0";
            }
        },
        trend() {
            const d = this.data.trend[this.attribute+"7DayChangePercent"] * 100;
            if (d > 5) {
                return {
                    rotate:
                        "padding-bottom: 0px; transform: translate(0px,8px) rotate(45deg) ",
                    icon: "fas fa-arrow-up",
                    color: "red",
                    hint: "Aufwärtstrend über 14 Tage"
                };
            } else if (d < -5) {
                return {
                    rotate: "transform: rotate(-45deg)",
                    icon: "fas fa-arrow-down",
                    color: "green",
                    hint: "Abwärtstrend über 14 Tage"
                };
            } else {
                return {
                    icon: "fas fa-minus",
                    color: "grey",
                    hint: "gleichbleibend über 14 Tage"
                };
            }
        }
    }
};
</script>