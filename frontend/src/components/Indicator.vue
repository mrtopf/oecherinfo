<template>
    <v-tooltip bottom max-width="300" color="rgba(0,0,0,1)">
        <template v-slot:activator="{ on }">
            <v-chip v-on="on" :dark="dark" class="my-1 ml-3" :color="color"
                >{{title}}: {{ value}}</v-chip
            >
        </template>
        {{ description }}
    </v-tooltip>

</template>
<script>
export default {
    props: {
        description: String,
        title: String,
        value: [Number, String],
        trend: Number, // -1,0,1
    },
    data() {
        return {
            
        }
    },
    computed: {
        dark() {
            if (this.trend==0) {
                return false
            } else if (this.trend==-1) {
                return true
            } else {
                return false
            }
        },
        color() {
            if (this.trend==0) {
                return "#F78656"
            } else if (this.trend==-1) {
                return "#960D2D"
            } else {
                return "#7FEDC4"
            }            
        }
    }
}
</script>