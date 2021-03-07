<template>
    <v-row>
        <v-col>
            <v-card tile>
                <v-toolbar dark dense flat color="primary">
                    <v-toolbar-title class="body-1 text-md-h6"
                        >Bettenbelegung</v-toolbar-title
                    >
                </v-toolbar>
                <v-card class="mt-5" color="#fff" flat :height="400">
                    <v-chart :option="options" ref="bar" autoresize />
                </v-card>

                <v-simple-table
                    class="mb-5"
                    dense
                    :class="
                        $vuetify.breakpoint.smAndUp
                            ? 'overview-table'
                            : 'overview-table small'
                    "
                >
                    <template v-slot:default>
                        <tbody>
                            <tr>
                                <th>COVID-19 Fälle</th>
                                <td>
                                    {{ data.today.covid19Cases }}
                                </td>
                            </tr>
                            <tr>
                                <th>davon beatmet</th>
                                <td>
                                    {{ data.today.ventilatorCases }}
                                </td>
                            </tr>
                            <tr>
                                <th>sonstige Fälle</th>
                                <td>
                                    {{
                                        data.today.occupiedBeds -
                                            data.today.covid19Cases
                                    }}
                                </td>
                            </tr>
                            <tr>
                                <th style="border-top: 2px solid black">belegte Betten</th>
                                <td style="border-top: 2px solid black" class="font-weight-bold">
                                    {{ data.today.occupiedBeds }}
                                </td>
                            </tr>
                            <tr class="">
                                <th>freie Betten</th>
                                <td>
                                    {{ data.today.freeBeds }}
                                    <v-badge dot :color="freeBedColor"></v-badge>
                                </td>
                            </tr>
                            <tr class="">
                                <th>Gesamtzahl Betten</th>
                                <td>
                                    {{ data.today.allBeds }}
                                </td>
                            </tr>

                        </tbody>
                    </template>
                </v-simple-table>

                <v-card-actions>
                    <v-btn
                        :to="{ name: 'hospitals' }"
                        tile
                        small
                        color="primary"
                        >Alle Daten einsehen</v-btn
                    >
                </v-card-actions>
            </v-card>
        </v-col>
        <v-col>
            <v-card tile class="text-left">
                <v-toolbar dark dense flat color="primary">
                    <v-toolbar-title class="body-1 text-md-h6"
                        >Intensivbetten</v-toolbar-title
                    >
                    <v-dialog v-model="hospitalHelp" scrollable width="700">
                        <template v-slot:activator="{ on, attrs }">
                            <v-btn
                                @click.capture="
                                    $matomo &&
                                        $matomo.trackEvent(
                                            'Corona',
                                            'hospital-info-click'
                                        )
                                "
                                color="white"
                                dark
                                v-bind="attrs"
                                v-on="on"
                                icon
                            >
                                <v-icon>fas fa-info-circle</v-icon>
                            </v-btn>
                        </template>

                        <v-card>
                            <v-card-title class="headline grey lighten-2">
                                Erklärungen
                                <v-spacer></v-spacer>
                                <v-btn
                                    color="grey"
                                    icon
                                    @click="hospitalHelp = false"
                                >
                                    <v-icon>fal fa-times</v-icon>
                                </v-btn>
                            </v-card-title>
                            <v-card-title
                                class="text-uppercase font-weight-bold"
                                >Status-Anzeigen</v-card-title
                            >

                            <v-card-text>
                                <table>
                                    <tr
                                        v-for="color in colors"
                                        :key="color.color"
                                    >
                                        <td>
                                            <v-badge
                                                :color="color.color"
                                                inline
                                                dot
                                            ></v-badge>
                                        </td>
                                        <td>{{ color.name }}</td>
                                    </tr>
                                </table>
                            </v-card-text>
                            <v-card-title
                                class="text-uppercase font-weight-bold"
                                >Begriffe</v-card-title
                            >
                            <v-card-text class="caption">
                                <h3 class="body-1 font-weight-bold">
                                    Low-Care-Behandlungsplatz
                                </h3>
                                <p>
                                    Intensivmedizinische Behandlungsplätze einer
                                    einfachen Versorgungsstufe.
                                </p>
                                <h4>
                                    Anforderung an die intensivmedizinische
                                    Austattung und Behandlungsmöglichkeiten
                                </h4>
                                <ul>
                                    <li>
                                        Basismonitoring (HF, RR, SpO2) mit
                                        High-Flow-Sauerstoff-Therapie und/oder
                                        nicht-invasiver Beatmung (NIV) und/oder
                                        tracheotomierte Patienten im Weaning
                                        sind möglich.
                                    </li>
                                    <li>
                                        <b
                                            >Invasive Beatmung im Rahmen der
                                            Akutversorgung ist nicht möglich.</b
                                        >
                                    </li>
                                </ul>
                                <h3 class="mt-5 body-1 font-weight-bold">
                                    High-Care-Behandlungsplatz
                                </h3>
                                <p>
                                    Intensivmedizinische Behandlungsplätze einer
                                    hohen Versorgungsstufe.
                                </p>
                                <h4>
                                    Anforderung an die intensivmedizinische
                                    Austattung und Behandlungsmöglichkeiten
                                </h4>
                                <ul>
                                    <li>
                                        Möglichkeit muss vorhanden sein für:
                                        <ul>
                                            <li>
                                                Basismonitoring (HF, RR, SpO2)
                                            </li>
                                            <li>
                                                differenzierte
                                                Katecholamintherapie
                                            </li>
                                            <li>
                                                differenzierte
                                                Katecholamintherapie
                                            </li>
                                            <li>
                                                kontrollierte invasive Beatmung
                                                mittels Intensivbeatmungsgeräten
                                                (über Endotrachealtubus oder
                                                Trachealkanüle) im Rahmen der
                                                Akutversorgung der
                                                respiratorischen Insuffizienz
                                                muss 24/7 möglich
                                            </li>
                                        </ul>
                                    </li>
                                    <li>
                                        Möglichkeit sollten vorhanden sein für:
                                        <ul>
                                            <li>
                                                Erweitertes Monitoring z.B.
                                                Echokardiographie oder
                                                Thermodilutionsverfahren
                                            </li>
                                            <li>
                                                Lagerungstherapie inklusive
                                                Bauchlagerung
                                            </li>
                                            <li>
                                                Möglichkeiten zur weiteren
                                                Organersatztherapie z.B.
                                                Nierenersatzverfahren
                                            </li>
                                        </ul>
                                    </li>
                                </ul>
                                <h3 class="mt-5 body-1 font-weight-bold">
                                    ECMO-Behandlungsplatz
                                </h3>
                                <p>
                                    Intensivmedizinische Behandlungsplätze der
                                    höchsten Versorgungsstufe.
                                </p>
                                <p>
                                    Höchste Versorgungsstufe unter Einsatz eines
                                    ECMO-Gerätes zur
                                    <a
                                        href="https://de.wikipedia.org/wiki/Extrakorporale_Membranoxygenierung"
                                        target="info"
                                        >extrakorporalen Membranoxygenierung</a
                                    >. ECMO ist nur auf einem High Care
                                    Behandlungsplatz möglich. Entsprechende
                                    apparative und personelle Ausstattung,
                                    fachliche Expertise wird vorausgesetzt
                                </p>
                            </v-card-text>
                            <v-card-text>
                                Die Daten stammen mit freundlicher Genehmigung
                                vom
                                <a
                                    href="https://www.intensivregister.de/"
                                    target="_blank"
                                    >DIVI Intensivregister</a
                                >.
                            </v-card-text>

                            <v-divider></v-divider>

                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn
                                    color="primary"
                                    text
                                    @click="hospitalHelp = false"
                                >
                                    Schliessen
                                </v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>
                </v-toolbar>

                <v-simple-table
                    dense
                    :class="
                        $vuetify.breakpoint.smAndUp
                            ? 'overview-table'
                            : 'overview-table small'
                    "
                >
                    <template v-slot:default>
                        <thead>
                            <tr>
                                <th
                                    :class="
                                        $vuetify.breakpoint.smAndUp
                                            ? 'black--text text-uppercase'
                                            : 'black--text text-uppercase px-1 py-1'
                                    "
                                >
                                    Krankenhaus
                                </th>
                                <th
                                    :class="
                                        $vuetify.breakpoint.smAndUp
                                            ? 'black--text text-center text-uppercase'
                                            : 'black--text text-uppercase px-1 py-1'
                                    "
                                >
                                    Low
                                </th>
                                <th
                                    :class="
                                        $vuetify.breakpoint.smAndUp
                                            ? 'black--text text-center text-uppercase'
                                            : 'black--text text-uppercase px-1 py-1'
                                    "
                                >
                                    High
                                </th>
                                <th
                                    :class="
                                        $vuetify.breakpoint.smAndUp
                                            ? 'black--text text-center text-uppercase'
                                            : 'black--text text-uppercase px-1 py-1'
                                    "
                                >
                                    ECMO
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="item in data.hospitals" :key="item.name">
                                <td
                                    :class="
                                        $vuetify.breakpoint.smAndUp
                                            ? 'body-2'
                                            : 'caption px-1 py-1'
                                    "
                                >
                                    {{ item.name }}
                                </td>
                                <td class="text-center">
                                    <v-badge
                                        :dot="!$vuetify.breakpoint.smAndUp"
                                        :color="item.lowCare"
                                    ></v-badge>
                                </td>
                                <td class="text-center">
                                    <v-badge
                                        :dot="!$vuetify.breakpoint.smAndUp"
                                        :color="item.highCare"
                                    ></v-badge>
                                </td>
                                <td class="text-center">
                                    <v-badge
                                        :dot="!$vuetify.breakpoint.smAndUp"
                                        :color="item.ecmo"
                                    ></v-badge>
                                </td>
                            </tr>
                        </tbody>
                    </template>
                </v-simple-table>
            </v-card>
        </v-col>
        <v-col class="caption text-right" cols="12"
            >Datenquelle:
            <a href="https://www.intensivregister.de/#/index"
                >DIVI Intensivregister</a
            ></v-col
        >
    </v-row>
</template>
<script>
import { format } from "echarts";

export default {
    props: {
        data: Object
    },
    data() {
        return {
            hospitalHelp: false,
            colors: [
                { color: "red", name: "voll" },
                { color: "oecheryellow", name: "begrenzt verfügbar" },
                { color: "green", name: "verfügbar" },
                {
                    color: "grey lighten-2",
                    name: "keine Angabe / nicht vorhanden"
                }
            ]
        };
    },
    computed: {
        date() {
            return this.data && format.formatTime("dd.MM.yyyy", this.data.date);
        },
        freeBedColor() {
            if (this.data.today.freeBeds < 5) {
                return "#960D2D"
            } else if (this.data.today.freeBeds < 10) {
                return "#F78656"                
            } else {
                return "#05C793"
            }
        },
        options() {
            return {
                grid: {
                    top: 0,
                    right: 0,
                    left: 0
                },
                title: {
                    subtext: `Stand ${this.date}`,
                    left: "center"
                },
                tooltip: {
                    trigger: "item"
                },
                textStyle: {
                    fontFamily: "JetBrains Mono"
                },
                series: [
                    {
                        top: 30,
                        name: "Bettenbelegung",
                        type: "pie",
                        radius: ["40%", "80%"],
                        colors: ["#0fa", "#fa0"],
                        startAngle: 70,
                        data: [
                            {
                                value:
                                    this.data.today.occupiedBeds -
                                    this.data.today.covid19Cases,
                                name: "sonstige Fälle",
                                itemStyle: { color: "#FFC43D" }
                            },
                            {
                                value: this.data.today.ventilatorCases,
                                name: "Beatmet, COVID-19",
                                itemStyle: { color: "#960D2D" }
                            },
                            {
                                value:
                                    this.data.today.covid19Cases -
                                    this.data.today.ventilatorCases,
                                name: "COVID-19-Fälle",
                                itemStyle: { color: "#F78656" }
                            },
                            {
                                value: this.data.today.freeBeds,
                                name: "freie Betten",
                                itemStyle: { color: "#05C793" }
                            }
                        ],
                        emphasis: {
                            itemStyle: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: "rgba(0, 0, 0, 0.5)"
                            }
                        }
                    }
                ]
            };
        }
    }
};
</script>