<template>
    <div class="home">
        <CoronaMain />
    </div>
</template>

<script>
// @ is an alias to /src
import CoronaMain from "@/components/CoronaMain.vue";

export default {
    name: "Home",
    components: {
        CoronaMain,
    },
};
</script>
