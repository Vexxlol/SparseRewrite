<template>
    <v-app style="background: #1F2133;">
        <Navbar style="z-index: 10; position: fixed; width: 100%;"/>
        <router-view style="margin-top: 5rem;"/>
    </v-app>
</template>

<script>
    import Navbar from "./components/Navbar";

    export default {
        name: 'App',

        components: {
            Navbar
        },
        data: () => ({
            //
        }),
    };
</script>
<style>
    html {
        scroll-behavior: smooth;
    }

    a {
        text-decoration: none;
    }

    ::-webkit-scrollbar {
        width: 12px;
    }

    ::-webkit-scrollbar-track {
        background: #b7b1b1;
    }

    ::-webkit-scrollbar-thumb {
        background: #5b5b5b;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #555;
    }
</style>