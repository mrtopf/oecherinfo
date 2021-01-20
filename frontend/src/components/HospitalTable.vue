<template>
    <v-row>
        <v-col>
            <v-card tile>
                <v-toolbar dark dense flat color="primary">
                    <v-toolbar-title class="body-1 text-md-h6"
                        >Überblick</v-toolbar-title
                    >
                </v-toolbar>

                <v-simple-table
                    v-if="divi.length>0"
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
                                <th>Anzahl Standorte</th>
                                <td>
                                    {{ divi[0].anzahl_standorte }}
                                </td>
                            </tr>
                            <tr>
                                <th>Verfügbare Betten</th>
                                <td>
                                    {{ divi[0].betten_belegt }}
                                </td>
                            </tr>
                            <tr>
                                <th>Freie Betten</th>
                                <td>
                                    {{ divi[0].betten_frei }}
                                </td>
                            </tr>
                            <tr>
                                <th>COVID-Fälle</th>
                                <td>
                                    {{ divi[0].faelle_covid_aktuell }}
                                </td>
                            </tr>
                            <tr>
                                <th>davon beatmet</th>
                                <td>
                                    {{ divi[0].faelle_covid_aktuell_beatmet }}
                                </td>
                            </tr>
                            <tr>
                                <th>Stand</th>
                                <td>
                                    {{ divi_date }}
                                </td>
                            </tr>
                        </tbody>
                    </template>
                </v-simple-table>
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
                                @click.capture="$matomo && $matomo.trackEvent('Corona', 'hospital-info-click')"
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
                                <th class="text-left">Krankenhaus</th>
                                <th class="text-left">Low</th>
                                <th class="text-left">High</th>
                                <th class="text-left">ECMO</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="item in hospitals" :key="item.name">
                                <td>
                                    {{ item.name }}
                                </td>
                                <td>
                                    <v-badge
                                        :dot="!$vuetify.breakpoint.smAndUp"
                                        :color="item.lowCare"
                                    ></v-badge>
                                </td>
                                <td>
                                    <v-badge
                                        :dot="!$vuetify.breakpoint.smAndUp"
                                        :color="item.highCare"
                                    ></v-badge>
                                </td>
                                <td>
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
import { mapState, mapActions, mapGetters } from "vuex";

export default {
    data() {
        return {
            hospitalHelp: false,
            colors: [
                { color: "red", name: "voll" },
                { color: "oecheryellow", name: "begrenzt verfügbar" },
                { color: "green", name: "verfügbar" },
                {
                    color: "grey lighten-2",
                    name: "keine Angabe / nicht vorhanden",
                },
            ],
        };
    },
    computed: {
        ...mapGetters("corona", ["muniName", "muni_data", "todayList"]),
        ...mapState({
            muniDict: (state) => state.corona.muniDict,
            loaded: (state) => state.corona.loaded,
            munis: (state) => state.corona.munis,
            divi: (state) => state.corona.divi,
            divi_date: (state) => state.corona.divi_date,
            hospitals: (state) => state.corona.hospitals,
            today: (state) => state.corona.today,
            yesterday: (state) => state.corona.yesterday,
            weekerday: (state) => state.corona.weekerday,
            date: (state) => state.corona.date,
            yesterdate: (state) => state.corona.yesterdate,
            selectedMuni: (state) => state.corona.selectedMuni,
        }),
    },
};
</script>