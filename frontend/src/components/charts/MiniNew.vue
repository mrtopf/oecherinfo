<template>
    <v-card class="mt-4 mx-auto" :loading="loading">
        <v-sheet
            class="v-sheet--offset mx-auto"
            :color="color"
            elevation="3"
            max-width="calc(100% - 24px)"
        >
            <v-sparkline
                v-if="propData != []"
                line-width="2"
                color="rgba(255,255,255,0.8)"
                :value="propData"
            ></v-sparkline>
        </v-sheet>

        <v-card-text class="pt-0">
            <div class="primary--text title font-weight-bold mb-2">{{title}}: {{ Math.round(propData[propData.length - 1]) }}</div>
        </v-card-text>
    </v-card>
</template>
<script>
export default {
    props: {
        prop: String,
        title: String,
        description: String,
        data: Object,
        small: Boolean,
        color: String,
        start: Number,
        dark: {
            type: Boolean,
            default: false,
        },
        loading: true,
    },
    computed: {
        miniClass() {
            if (this.small) {
                return "font-weight-thin text-uppercase text-h6";
            } else {
                return "font-weight-thin text-uppercase text-h3";
            }
        },
        propData() {
            if (!this.data) {
                return [];
            }
            const d = this.data[this.prop];
            return d.slice(this.start, 999999);
        },
    },
};
</script>
<style>
  .v-sheet--offset {
    top: -24px;
    position: relative;
  }
</style>
