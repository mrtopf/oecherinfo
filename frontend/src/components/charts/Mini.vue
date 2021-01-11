<template>
    <v-card :color="color" :loading="loading" flat @click="$emit('click')">
        <v-toolbar :dense="noDetails" :color="color" :dark="dark" flat >
            <v-toolbar-title :class="miniClass" >
                {{ title }}
                <template  v-if="!noDetails">
                : {{ Math.round(propData[propData.length - 1]) }}
                <small v-if="newValue - oldValue > 0"
                    >+{{ Math.round(newValue - oldValue) }}</small
                >
                <small v-if="newValue - oldValue < 0">{{
                    Math.round(newValue - oldValue)
                }}</small>
                    </template> 
            </v-toolbar-title>
        </v-toolbar>

        <v-card-text class="text-left">
            <v-sparkline
                @click="$emit('click')"
                v-if="propData != []"
                    auto-draw
                line-width="2"
                :color="!dark? 'rgba(0,0,0,0.3)' : 'rgba(255,255,255,0.8)'"
                :value="propData"
            ></v-sparkline>
        </v-card-text>
    </v-card>
</template>
<script>
export default {
    props: {
        prop: String,
        title: String,
        yesterdate: String,
        description: String,
        data: Object,
        small: Boolean,
        color: String,
        start: Number,
        oldValue: Number,
        newValue: Number,
        'no-details': Boolean,
        dark: {
            type: Boolean,
            default: false,
        },
        loading: true,
    },
    computed: {
        miniClass() {
            if (this.noDetails) {
                return "small-headline text-uppercase";
            }
            else if (this.small || this.noDetails) {
                return "mini-headline font-weight-thin text-uppercase text-h6";
            } else {
                return "mini-headline font-weight-bold text-uppercase text-lg-h4";
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
<style lang="scss">
.data-headline > div {
    font-size: 85%;
    font-weight: 400;
    margin: 0;
    padding: 0;
    color: white;
    text-align: right;
}
.small-headline {
    font-size: 14px;
}
.mini-headline {
    span {
        font-weight: 200;
        font-size: 60%;
    }
    small {
        font-size: 60%;

    }

}
</style>
